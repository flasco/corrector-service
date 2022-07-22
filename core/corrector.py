import functools
import torch
import time
from transformers import BertTokenizer, BertForMaskedLM
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None
tokenizer = None
inited = False

def init_model():
    global model, tokenizer, device, inited
    if (inited):
        return
    inited = True
    tokenizer = BertTokenizer.from_pretrained("./model")
    model = BertForMaskedLM.from_pretrained("./model")
    model.to(device)

    with torch.no_grad():
        print('model init succeed')

def cmp(a,b):
    return a["start"] - b["start"];

def get_errors(corrected_text, origin_text):
    sub_details = []
    for i, ori_char in enumerate(origin_text):
        if ori_char in [' ', '“', '”', '‘', '’', '琊', '\n', '…', '—', '擤']:
            # add unk word
            corrected_text = corrected_text[:i] + ori_char + corrected_text[i:]
            continue
        if i >= len(corrected_text):
            continue
        if ori_char != corrected_text[i]:
            if ori_char.lower() == corrected_text[i]:
                # pass english upper char
                corrected_text = corrected_text[:i] + ori_char + corrected_text[i + 1:]
                continue
            sub_details.append({
                "before": ori_char,
                "after": corrected_text[i],
                "start": i,
                "end": i + 1
            })
    sub_details = sorted(sub_details, key=functools.cmp_to_key(cmp))
    return corrected_text, sub_details

def check_corrector(cur_text):
    if model == None or tokenizer == None:
        return { "message": "please wait while initializing" }

    with torch.no_grad():
        stamp = time.time()
        outputs = model(**tokenizer([cur_text], padding=True, return_tensors='pt').to(device))
        cost = time.time() - stamp
        result = []

        for ids, text in zip(outputs.logits, [cur_text]):
            _text = tokenizer.decode(torch.argmax(ids, dim=-1), skip_special_tokens=True).replace(' ', '')
            corrected_text = _text[:len(text)]
            corrected_text, details = get_errors(corrected_text, text)
            print(text, ' => ', corrected_text, details)
            result.append({ "corrected": corrected_text, "details": details})
        return { "result": result, "cost": '{:.2f}ms'.format(cost * 1000) }
