import sys
import os

sys.path.append('/home/gene/Documents/Senti/Comment/TransE/OpenKE')

import time
import torch
from OpenKE.openke.config import Trainer, Tester
from OpenKE.openke.module.model import TransE
from OpenKE.openke.module.loss import MarginLoss
from OpenKE.openke.module.strategy import NegativeSampling
from OpenKE.openke.data import TrainDataLoader, TestDataLoader
from bertmodel import load_emb
from utils import save_data

# embed entities
def embed_entity(embedding_layer, n_ent, emb_dim = 768):
    ent_ids = torch.tensor(list(range(n_ent)), dtype = int, device = 'cuda')
    ent_embeds = torch.zeros((n_ent, emb_dim))
    batch_size = 16
    begin = 0
    while begin < n_ent:
        end = min(n_ent, begin + batch_size)
        ent_embeds[begin: end] = embedding_layer(ent_ids[begin: end])
        begin += batch_size
    return ent_embeds

# def dump_entity_embeds(embedding_layer, file_path):
# 	ent_embeds = embed_entity(embedding_layer, n_ent)

def train(transe, train_dataloader, test_dataloader = None, nbatches = 1000):
	model = NegativeSampling(
		model = transe, 
		loss = MarginLoss(margin = 5.0), # define the loss function
		batch_size = train_dataloader.get_batch_size()
	)

	# train the model
	trainer = Trainer(model = model, data_loader = train_dataloader, train_times = nbatches, alpha = 1.0, use_gpu = True)
	trainer.run()
	model_time = time.strftime('%m%d%H%M', time.localtime())
	transe.save_checkpoint('./result/transe_{}.ckpt'.format(model_time))
	print('Save model: ', model_time)

	# test
	if test_dataloader is not None:
		tester = Tester(model = transe, data_loader = test_dataloader, use_gpu = True)
		mrr, mr, hit10, hit3, hit1 = tester.run_link_prediction(type_constrain = True)
	return transe, model_time

def train_transe(n_ent, n_rel, data_path = './data/', mod = 'bert', emb_time = '10251007', emb_dim = 768, nbatches = 1000):
	train_dataloader = TrainDataLoader(
		in_path = data_path, 
		nbatches = nbatches,
		threads = 8, 
		sampling_mode = "normal", 
		bern_flag = 1, 
		filter_flag = 1, 
		neg_ent = 25,
		neg_rel = 0)
	test_dataloader = TestDataLoader(data_path, "link", True)

	if mod == 'bert' or mod == 'bert-transe':
		bert_emb, rel_emb = load_emb(emb_time)
		pretrain_emb = [bert_emb, rel_emb]
	else:
		pretrain_emb = None
	
	transe = TransE(
		ent_tot = train_dataloader.get_ent_tot(), # total number of entity
		rel_tot = train_dataloader.get_rel_tot(),
		dim = emb_dim, 
		p_norm = 1, 
		norm_flag = True,
		pretrain_emb = pretrain_emb
		).cuda()

	transe, model_time = train(transe, train_dataloader, test_dataloader)
	ent_emb = embed_entity(transe.ent_embeddings, n_ent, emb_dim)
	rel_emb = embed_entity(transe.rel_embeddings, n_rel, emb_dim)
	if mod == 'bert' or mod == 'bert-transe':
		emb_time = save_data('./result/bert_transe_emb.vec', [ent_emb, rel_emb], model_time)
	else:
		emb_time = save_data('./result/transe_emb.vec', [ent_emb, rel_emb], model_time)
	return transe, model_time, ent_emb, rel_emb, emb_time

def get_transe_embeds(model_time, n_ent, n_rel, mod = 'bert', emb_dim = 768):
	transe = TransE(
		ent_tot = n_ent, # total number of entity
		rel_tot = n_rel,
		dim = emb_dim, 
		p_norm = 1, 
		norm_flag = True
	).cuda()
	transe.load_checkpoint('./result/transe_{}.ckpt'.format(model_time))
	ent_emb = embed_entity(transe.ent_embeddings, n_ent, emb_dim)
	rel_emb = embed_entity(transe.rel_embeddings, n_rel, emb_dim)
	print('Load model:', model_time, ', ent_emb:', ent_emb.shape, ', rel_emb:', rel_emb.shape)
	if mod == 'bert-transe':
		save_data('./result/bert_transe_emb.vec', [ent_emb, rel_emb], data_time = model_time)
	else:
		save_data('./result/transe_emb.vec', [ent_emb, rel_emb], data_time = model_time)
	return ent_emb, rel_emb, model_time

if __name__ == '__main__':
	train_transe('bert')
