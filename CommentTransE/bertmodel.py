import numpy as np
import os
import pickle
import time
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from transformers import BertTokenizer, BertModel
from AttentionModel import AttentionPooling
from pytorchtools import EarlyStopping
from utils import save_data, load_data

bert_path = '/data/pretrained/'

class BertCls(nn.Module):
    def __init__(self, n_type):
        super().__init__()
        self.bert = BertModel.from_pretrained(bert_path + 'bert-base-chinese/').to('cuda')
        self.avg = AttentionPooling(768, 200)
        self.dropout = nn.Dropout(0.2)
        self.cls = nn.Linear(768, n_type)
    def forward(self, token_ids, mask_ids):
        bert_out = self.bert(token_ids, mask_ids)['last_hidden_state'] # (n_batch, n_tokens, n_emb)
        bert_out = self.dropout(bert_out)
        bert_out = self.avg(bert_out)
        cls_out = self.cls(bert_out)
        return cls_out
    def embedding(self, token_ids, mask_ids):
        bert_out = self.bert(token_ids, mask_ids)['last_hidden_state'] # (n_batch, n_tokens, n_emb)
        bert_out = self.dropout(bert_out)
        bert_out = self.avg(bert_out)
        return bert_out # (n_batch, n_emb)

class BertData():
    def __init__(self, tokens, masks, label, batch_size = 16):
        self.tokens = tokens
        self.masks = masks
        self.label = torch.tensor(label, dtype = torch.long)
        self.batch_size = batch_size
    
    def __len__(self):
        return np.ceil(len(self.tokens) / self.batch_size)

    def __getitem__(self, i):
        begin = i * self.batch_size
        end = min(begin + self.batch_size, len(self.tokens))
        tokens = self.tokens[begin: end].to('cuda')
        masks = self.masks[begin: end].to('cuda')
        label = self.label[begin: end].to('cuda')
        return tokens, masks, label

def save_model(model, vocab, path = './result/'):
    model_time = '{}'.format(time.strftime('%m%d%H%M', time.localtime()))
    model_path = path + '{}'.format(model_time)
    os.mkdir(model_path)
    torch.save(model.state_dict(), model_path + '/model_' + model_time)
    with open(model_path + '/vocab_' + model_time, 'wb') as f:
        pickle.dump(vocab, f)
    print('Save model:', model_path)
    return model_time

def load_model(model_time, model):
    model_path = './result/{}'.format(model_time)
    model.load_state_dict(torch.load(model_path + '/model_' + model_time))
    with open(model_path + '/vocab_' + model_time, 'rb') as f:
        vocab = pickle.load(f)
    return model, vocab

def train_bert(train_loader, valid_loader, n_type):
    model = BertCls(n_type).to('cuda')
    optimizer = optim.Adam(model.parameters(), lr = 3e-6)
    early_stopping = EarlyStopping(patience = 5, verbose = False)
    entrophy = nn.CrossEntropyLoss()
    epochs = 100
    avg_train_losses = []
    avg_valid_losses = []
    train_correct, train_total, valid_correct, valid_total = 0, 0, 0, 0
    for epoch in range(epochs):
        train_losses = []
        valid_losses = []
        model.train()
        for _, batch in tqdm(enumerate(train_loader)):
            if(len(batch[0]) == 0):
                break
            tokens, masks, labels = batch
            optimizer.zero_grad()
            output = model(tokens, masks) # (n_batch, n_class)
            loss = entrophy(output, labels)
            train_losses.append(loss.item())
            loss.backward()
            optimizer.step()
            predict = torch.max(output, dim = 1).indices # (n_batch)
            train_correct += torch.sum(predict == labels).item()
            train_total += len(labels)
        avg_train_loss = np.average(train_losses)
        avg_train_losses.append(avg_train_loss)

        model.eval()
        with torch.no_grad():
            for i, batch in enumerate(valid_loader):
                if(len(batch[0]) == 0):
                    break
                tokens, masks, labels = batch
                output = model(tokens, masks)
                loss = entrophy(output, labels)
                valid_losses.append(loss.item())
                predict = torch.max(output, dim = 1).indices # (n_batch, n_tokens)
                valid_correct += torch.sum(predict == labels).item()
                valid_total += len(labels)
            avg_valid_loss = np.average(valid_losses)
            avg_valid_losses.append(avg_valid_loss)
        
        print('[epoch {:d}] TrainLoss: {:.4f} DevLoss: {:.4f} TAcc: {:.3f} VAcc: {:.3f}'.format(
            epoch + 1, avg_train_loss, avg_valid_loss, train_correct / train_total, valid_correct / valid_total))
        early_stopping(valid_correct / valid_total, model)
        if early_stopping.early_stop:
            print("Early stopping")
            break
    return model

def test_bert(model, test_set):
    test_correct, test_total = 0, 0
    model.eval()
    with torch.no_grad():
        for _, batch in enumerate(test_set):
            if(len(batch[0]) == 0):
                break
            tokens, masks, labels = batch
            output = model(tokens, masks)
            predict = torch.max(output, dim = 1).indices # (n_batch, n_tokens)
            test_correct += torch.sum(predict == labels).item()
            test_total += len(labels)
    print('Test: Acc: {:4f}'.format(test_correct / test_total))

def train_bertcls_emb(ent_dict, ent_label_list, n_type, rel_type_list):
    tokenizer = BertTokenizer.from_pretrained(bert_path + 'bert-base-chinese/')
    tokens = tokenizer([ent for ent in ent_dict], 
                       padding = 'max_length', truncation = True, max_length = 20, return_tensors = 'pt')
    
    n_train = int(0.8 * len(tokens['input_ids']))
    train_set = BertData(tokens['input_ids'][:n_train], tokens['attention_mask'][:n_train], ent_label_list[:n_train])
    valid_set = BertData(tokens['input_ids'][n_train:], tokens['attention_mask'][n_train:], ent_label_list[n_train:])
    model = train_bert(train_set, valid_set, n_type)

    vocab = [tokenizer, tokens]
    model_time = save_model(model, vocab)
    test_bert(model, valid_set)
    bert_emb, rel_emb, emb_time = get_bertcls_emb(rel_type_list, n_type, model_time)

    return model, model_time, bert_emb, rel_emb, emb_time

def get_bertcls_emb(rel_type_list, n_type, model_time = '10221520'):
    model = BertCls(n_type).to('cuda')
    model, vocab = load_model(model_time, model)
    tokenizer, tokens = vocab

    batch_size = 16
    bert_emb = []
    for i in range(0, len(tokens['input_ids']), batch_size):
        token_ids = tokens['input_ids'][i: i + batch_size].to('cuda')
        mask_ids = tokens['attention_mask'][i: i + batch_size].to('cuda')
        bert_out = model.embedding(token_ids, mask_ids) # (n_batch, n_tokens, n_emb)
        bert_emb.append(bert_out.detach().cpu())
    bert_emb = torch.cat(bert_emb, dim = 0) # ([81607, 768])

    
    rel_tokens = tokenizer([rel for rel in rel_type_list], 
                       padding = 'max_length', truncation = True, max_length = 20, return_tensors = 'pt')
    token_ids = rel_tokens['input_ids'].to('cuda')
    mask_ids = rel_tokens['attention_mask'].to('cuda')
    bert_out = model.embedding(token_ids, mask_ids) # (n_batch, n_tokens, n_emb)
    rel_emb = bert_out.detach().cpu()

    emb_time = save_data('./result/bert_emb.vec', [bert_emb, rel_emb])
    print('bert_emb:', bert_emb.shape, 'rel_emb:', rel_emb.shape)
    return bert_emb, rel_emb, emb_time

def load_emb(emb_time):
    ent_emb, rel_emb = load_data('./result/bert_emb.vec', emb_time)
    return ent_emb, rel_emb

if __name__ == '__main__':
    from load_dataset import define_entity, define_relation, load_dataset
    label_list = define_entity() # ['Product', 'Target', 'Opinion', 'Category', 'Polarity']
    rel_type_list = [trip[2] for trip in define_relation()] # ['评价产品', '产品评价词', '评价', '评价类别', '类别评价词', '评价极性']

    ent_list, rel_list, train_list, valid_list, test_list, ent_label_list = load_dataset('./data/')

    # bert_emb, rel_emb, emb_time = get_bertcls_emb(rel_type_list, ent_type_dict, '10271539')
    model, model_time, bert_emb, rel_emb, emb_time = train_bertcls_emb(ent_list, ent_label_list, len(label_list), rel_type_list)

