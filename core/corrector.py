import operator
import torch
import time
from transformers import BertTokenizer, BertForMaskedLM
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None
tokenizer = None

def init_model():
    global model, tokenizer, device
    tokenizer = BertTokenizer.from_pretrained("shibing624/macbert4csc-base-chinese")
    model = BertForMaskedLM.from_pretrained("shibing624/macbert4csc-base-chinese")
    model.to(device)

    with torch.no_grad():
        print('model init succeed')

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
            sub_details.append((ori_char, corrected_text[i], i, i + 1))
    sub_details = sorted(sub_details, key=operator.itemgetter(2))
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
            result.append({ "corrected": corrected_text, "position": details})
        return { "result": result, "cost": '{:.2f}ms'.format(cost * 1000) }
