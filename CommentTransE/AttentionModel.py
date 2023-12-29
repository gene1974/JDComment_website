import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class AttentionPooling(nn.Module):
    def __init__(self, emb_dim, query_dim):
        super().__init__()
        self.fc1 = nn.Linear(emb_dim, query_dim)
        self.fc2 = nn.Linear(query_dim, 1)
        
    def forward(self, x, mask = None):
        '''
        (n_batch, n_seq, emb_dim) -> (n_batch, emb_dim)
        a = q^T tanh(V * k + v)
        alpha = softmax(a)
        '''
        a = self.fc2(torch.tanh(self.fc1(x))) # (n_batch, n_seq, 1)
        if mask is not None:
            a = a.masked_fill(mask.unsqueeze(-1) == 0, -1e9)
        alpha = F.softmax(a, dim = -2) # (n_batch, n_seq, 1)
        r = torch.matmul(alpha.transpose(-2, -1), x).squeeze(-2) # (n_batch, emb_dim)
        return r

class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_k):
        super().__init__()
        self.d_k = d_k

    def forward(self, Q, K, V, attn_mask=None):
        scores = torch.matmul(Q, K.transpose(-1, -2)) / np.sqrt(self.d_k)
        scores = torch.exp(scores)
        if attn_mask is not None:
            scores = scores * attn_mask
        attn = scores / (torch.sum(scores, dim=-1, keepdim=True)  + 1e-8)
        
        context = torch.matmul(attn, V)
        return context, attn

class MultiHeadSelfAttention(nn.Module):
    def __init__(self, d_model, n_heads, d_k, d_v):
        super().__init__()
        self.d_model = d_model # 300
        self.n_heads = n_heads # 20
        self.d_k = d_k # 20
        self.d_v = d_v # 20
        
        self.W_Q = nn.Linear(d_model, d_k * n_heads) # 300, 400
        self.W_K = nn.Linear(d_model, d_k * n_heads) # 300, 400
        self.W_V = nn.Linear(d_model, d_v * n_heads) # 300, 400
        
        self._initialize_weights()
                
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight, gain=1)
                
    def forward(self, Q, K, V, attn_mask=None):
        residual, batch_size = Q, Q.size(0)
        
        q_s = self.W_Q(Q).view(batch_size, -1, self.n_heads, self.d_k).transpose(1,2)
        k_s = self.W_K(K).view(batch_size, -1, self.n_heads, self.d_k).transpose(1,2)
        v_s = self.W_V(V).view(batch_size, -1, self.n_heads, self.d_v).transpose(1,2)
        
        # if attn_mask is not None:
        #     attn_mask = attn_mask.unsqueeze(1).expand(batch_size, max_len, max_len) 
        #     attn_mask = attn_mask.unsqueeze(1).repeat(1, self.n_heads, 1, 1) 
        
        context, attn = ScaledDotProductAttention(self.d_k)(q_s, k_s, v_s, attn_mask) 
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.n_heads * self.d_v) 
        return context # (n_batch, n_seq, emb_dim)


