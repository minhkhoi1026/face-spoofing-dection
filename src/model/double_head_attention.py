from sklearn.preprocessing import LabelEncoder
import torch
from torch import nn

from src.extractor import EXTRACTOR_REGISTRY
from src.model.abstract import AbstractModel
from src.loss import LOSS_REGISTRY
from src.model.feat_attention import FeatAttention

class DoubleHeadAttentionFrameClassifier(AbstractModel):
    def init_model(self):
        extractor_cfg = self.cfg["model"]["extractor"]
        
        self.img_extractor = EXTRACTOR_REGISTRY.get(extractor_cfg["img_encoder"]["name"])(
            **extractor_cfg["img_encoder"]["args"]
        )
        embed_dim = self.img_extractor.feature_dim
        
        self.mlp = nn.Linear(embed_dim, self.cfg["model"]["num_classes"])

        self.loss = LOSS_REGISTRY.get(self.cfg["loss"]["name"])(
            **self.cfg["loss"]["args"]
        )
        
    def forward(self, batch):
        # dim=1 means concatenate along the channel dimension
        combined_batch = torch.cat((batch["imgs"], batch["img_variants"]), dim=1)
        feat = self.img_extractor(combined_batch)
        logits = self.mlp(feat)

        return {
            "logits": logits
        }

    def compute_loss(self, forwarded_batch, input_batch):
        logits, labels = forwarded_batch["logits"], input_batch["labels"]
        return self.loss(logits, labels)
    
    def extract_target_from_batch(self, batch):
        return batch["labels"].argmax(dim=1)
    
    def extract_pred_from_forwarded_batch(self, forwarded_batch):
        # change to probability since raw logits are passed
        preds = nn.Softmax(dim=1)(forwarded_batch["logits"])
        preds = preds[:, 1]  
        return preds
