# -*- coding: utf-8 -*-
"""DIP PROJECT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ogFytH2VeIm6QgBDiuAQoHAo7ALQXSnP
"""

#!pip install -Uqq fastbook
import fastbook
fastbook.setup_book()

!pip install anvil-uplink

import anvil.server

anvil.server.connect("BIORY47T4WFDI2QFOHAEAV4Y-K2L7QDB2BX3UIAU2")

from fastbook import *
from fastai.vision.widgets import *

!pip install jmd_imagescraper

from jmd_imagescraper.core import *
from pathlib import Path

root = Path().cwd()/"ice creams"

duckduckgo_search(root, "Vanilla", "Vanilla ice cream", max_results=200)
duckduckgo_search(root, "Chocolate", "Chocolate ice cream", max_results=200)
duckduckgo_search(root, "Strawberry", "Strawberry ice cream", max_results=200)
duckduckgo_search(root, "Mango", "Mango ice cream", max_results=200)

path = Path('ice creams')
fns = get_image_files(path)
fns

failed = verify_images(fns)
failed

failed.map(Path.unlink);

class DataLoaders(GetAttr):
    def __init__(self, *loaders): self.loaders = loaders
    def __getitem__(self, i): return self.loaders[i]
    train,valid = add_props(lambda i,self: self[i])

icecreams = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.3, seed=42),
    get_y=parent_label,
    item_tfms=Resize(128))

dls = icecreams.dataloaders(path)

dls.valid.show_batch(max_n=6, nrows=1)

icecreams = icecreams.new(item_tfms=Resize(128, ResizeMethod.Squish))
dls = icecreams.dataloaders(path)
dls.valid.show_batch(max_n=6, nrows=1)

icecreams = icecreams.new(item_tfms=Resize(128, ResizeMethod.Pad, pad_mode='zeros'))
dls = icecreams.dataloaders(path)
dls.valid.show_batch(max_n=6, nrows=1)

icecreams = icecreams.new(item_tfms=RandomResizedCrop(128, min_scale=0.3))
dls = icecreams.dataloaders(path)
dls.train.show_batch(max_n=4, nrows=1, unique=True)

icecreams = icecreams.new(item_tfms=Resize(128), batch_tfms=aug_transforms(mult=2))
dls = icecreams.dataloaders(path)
dls.train.show_batch(max_n=8, nrows=2, unique=True)

icecreams = icecreams.new(
    item_tfms=RandomResizedCrop(224, min_scale=0.5),
    batch_tfms=aug_transforms())
dls = icecreams.dataloaders(path)

icecreams = icecreams.new(
    item_tfms=RandomResizedCrop(224, min_scale=0.5),
    batch_tfms=aug_transforms())
dls = icecreams.dataloaders(path)

learn = cnn_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(4)

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

interp.plot_top_losses(10, nrows=2)

cleaner = ImageClassifierCleaner(learn)
cleaner

for idx in cleaner.delete(): cleaner.fns[idx].unlink()

for idx,cat in cleaner.change(): shutil.move(str(cleaner.fns[idx]), path/cat)

btn_upload = widgets.FileUpload()
btn_upload

img = PILImage.create(btn_upload.data[-1])
pred,pred_idx,probs = learn.predict(img)
lbl_pred = widgets.Label()
lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
lbl_pred

btn_run = widgets.Button(description='Classify')
btn_run

def on_click_classify(change):
    img = PILImage.create(btn_upload.data[-1])
    out_pl.clear_output()
    with out_pl: display(img.to_thumb(128,128))
    pred,pred_idx,probs = learn.predict(img)
    lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'

btn_run.on_click(on_click_classify)

btn_upload = widgets.FileUpload()
out_pl = widgets.Output()
out_pl.clear_output()
with out_pl: display(img.to_thumb(128,128))
out_pl

lbl_pred = widgets.Label()
lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
lbl_pred

VBox([widgets.Label('Choose your ice cream!'), 
      btn_upload, btn_run, out_pl, lbl_pred])

learn.export()

path = Path()
path.ls(file_exts='.pkl')

learn_inf = load_learner(path/'export.pkl')

learn_inf.predict('/content/images/035.-Mango-Ice-Cream_545x545.png')

@anvil.server.callable
def predict(sepal_length, sepal_width, petal_length, petal_width):
  classification = knn.predict([[sepal_length, sepal_width, petal_length, petal_width]])
  return iris.target_names[classification][0]

anvil.server.wait_forever()