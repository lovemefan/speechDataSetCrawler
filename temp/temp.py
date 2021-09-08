# -*- coding: utf-8 -*-
# @Time  : 2021/4/19 10:03
# @Author : lovemefan
# @File : temp.py
cbd = "阿富汗，阿尔巴尼亚，阿尔及利亚，安哥拉，安提瓜和巴布达，阿根廷，亚美尼亚，澳大利亚，奥地利，阿塞拜疆，巴哈马，巴林，孟加拉国，巴巴多斯，白俄罗斯，比利时，伯利兹，贝宁，不丹，玻利维亚，波斯尼亚和黑塞哥维那，博茨瓦纳，巴西，文莱达鲁萨兰国，保加利亚，布基纳法索，缅甸，布隆迪，柬埔寨，喀麦隆，加拿大，佛得角，中华人民共和国，中非共和国，乍得，智利，哥伦比亚，科摩罗，刚果共和国，刚果共和国，库克群岛，哥斯达黎加，科特迪瓦，克罗地亚，古巴，塞浦路斯，捷克共和国，丹麦，吉布提，多米尼加，多米尼加共和国，厄瓜多尔，埃及，萨尔瓦多，赤道几内亚，厄立特里亚，爱沙尼亚，埃塞俄比亚，欧盟，斐济，芬兰，法国，加蓬，冈比亚，格鲁吉亚，德国，加纳，希腊，格林纳达，危地马拉，几内亚，几内亚比绍，圭亚那，海地，洪都拉斯，匈牙利，冰岛，印度，印度尼西亚，伊朗，伊拉克，爱尔兰，以色列，意大利，牙买加，日本，约旦，哈萨克斯坦，肯尼亚，基里巴斯，科威特，朝鲜，韩国，吉尔吉斯斯坦，老挝，拉脱维亚，黎巴嫩，莱索托，利比里亚，利比亚，列支敦士登，立陶宛，卢森堡，马其顿共和国，马达加斯加，马拉维，马来西亚，马尔代夫，马里，马耳他，马绍尔群岛，毛里塔尼亚，毛里求斯，墨西哥，密克罗尼西亚联邦，摩尔多瓦，摩纳哥，蒙古，黑山，摩洛哥，莫桑比克，纳米比亚，瑙鲁，尼泊尔，荷兰，新西兰，尼加拉瓜，尼日尔，尼日利亚，纽埃，挪威，阿曼，巴基斯坦，帕劳，巴拿马，巴布亚新几内亚，巴拉圭，秘鲁，菲律宾，波兰，葡萄牙，卡塔尔，罗马尼亚，俄罗斯，卢旺达，圣基茨和尼维斯，圣卢西亚，圣文森特和格林纳丁斯，萨摩亚，圣马力诺，圣多美和普林西比，沙特阿拉伯，塞内加尔，塞尔维亚，塞舌尔，塞拉利昂，新加坡，斯洛伐克，斯洛文尼亚，所罗门群岛，索马里，南非，西班牙，斯里兰卡，苏丹，苏里南，斯威士兰，瑞典，瑞士，叙利亚，塔吉克斯坦，坦桑尼亚，泰国，东帝汶，多哥，汤加，特立尼达和多巴哥，突尼斯，土耳其，土库曼斯坦，图瓦卢，乌干达，乌克兰，阿拉伯联合酋长国，英国，乌拉圭，乌兹别克斯坦，瓦努阿图，委内瑞拉，越南，也门，赞比亚，津巴布韦，南苏丹，巴勒斯坦，安道尔"
cbd_countrys = cbd.split('，')


list = []
countrys = {}
with open('tts.txt', 'r', encoding='utf-8') as f:
    for line in f:

        country, model, lang_code, tts_code, gender = line.split('\t')
        if not countrys.get(country.split('（')[0], None) and model == '标准':
            countrys[country.split('（')[0]] = {}
            countrys[country.split('（')[0]]['lang_code'] = lang_code
            countrys[country.split('（')[0]]['tts_code'] = lang_code
            countrys[country.split('（')[0]]['gender_code'] = (gender, tts_code)


with open('asr.txt', 'r', encoding='utf-8') as f:
    for line in f:
        res = line.split('\t')
        country, lang_code = res[0], res[1]
        if not countrys.get(country.split('（')[0], None):
            countrys[country.split('（')[0]] = {}
        countrys[country.split('（')[0]]['lang_code'] = lang_code
        countrys[country.split('（')[0]]['asr_code'] = lang_code

for key in countrys.keys():
    if key.replace('语', '') in cbd_countrys:
        countrys[key]['is_cdb'] = True
        print(key)
    else:
        countrys[key]['is_cdb'] = False

