#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import ast
import datetime
from . import api
from flask import jsonify, request
from dateutil.parser import parse
from app.lib.JDComment.event_model import EVENTMODEL
from app.lib.event_manager import EVENT
from collections import Counter

# @api.route('/getDailyInfo1', methods=['POST'])
# def get_daily_info1():
#     location = request.get_json()["location"]
#     variety = request.get_json()["variety"]
#     start_date = request.get_json()["start_date"]
#     end_date = request.get_json()["end_date"]
#     print(location)
#     print(variety)
#     print(start_date)
#     print(end_date)
#     result = EVENT.get_daily_info(location, variety, start_date, end_date)
#     result = sorted(result, key=lambda x: x["date"], reverse=False)
#     return jsonify({'code':200, 'msg':'查询成功', 'data':result})

def get_info_text(result, variety, avg_score, avg_heat):
    if avg_score > 4:
        result['score_text'] = '消费者对{}整体非常满意，综合评分为{:.2f}。'.format(variety, avg_score)
    elif avg_score > 3:
        result['score_text'] = '消费者对{}整体较为满意，综合评分为{:.2f}。'.format(variety, avg_score)
    elif avg_score > 2:
        result['score_text'] = '消费者对{}整体评价一般，综合评分为{:.2f}。'.format(variety, avg_score)
    elif avg_score > 1:
        result['score_text'] = '消费者对{}整体较不满意，综合评分为{:.2f}。'.format(variety, avg_score)
    else:
        result['score_text'] = '消费者对{}整体非常不满意，综合评分为{:.2f}。'.format(variety, avg_score)
    
    if avg_heat > 4:
        result['heat_text'] = '{}评价热度很高，平均每天{:.2f}条评价。'.format(variety, avg_heat)
    elif avg_heat > 3:
        result['heat_text'] = '{}评价热度较高，平均每天{:.2f}条评价。'.format(variety, avg_heat)
    elif avg_heat > 2:
        result['heat_text'] = '{}评价热度一般，平均每天{:.2f}条评价。'.format(variety, avg_heat)
    elif avg_heat > 1:
        result['heat_text'] = '{}评价热度较低，平均每天{:.2f}条评价。'.format(variety, avg_heat)
    else:
        result['heat_text'] = '{}评价热度很低，平均每天小于1条评价。'.format(variety, avg_heat)

def get_fixed_advice(result, variety):
    variety_advice = {
        '大米':'水稻的生长过程中需水量很大，适宜种植在高温多雨的地区。', 
        '茶叶':'茶树喜欢弱光、散光，而非强光、直射光。茶园周边要种防护林，道路旁种行道树，茶园行间种遮荫树，灌水最好是喷灌。夏秋天，光线太强，温度又高，做成的夏秋茶苦涩味太浓，做红茶可以，做绿茶不是很好。', 
        '蜜柚':'蜜柚喜欢温暖潮湿的环境，要是能在疏松肥沃的土壤上种植，蜜柚的产量会更高。', 
        '花生':'花生不耐盐碱，避免重茬，否则会造成病虫害，容易造成营养元素缺失，品质差等问题，前茬药以甘薯，玉米，水稻等，避免和豆科类的作物进行轮作。也可以和禾本科的作物进行轮作，一般三年轮作一次，选择土壤丰厚，土壤疏松，比较肥沃的地块，土壤深度至少保证30公分以上，PH值在7.0左右，这样有利于花生根系的发育和品质。', 
        '玉米':'玉米种子需要选择色泽饱满，籽粒均匀，没有破损的优质种子。玉米拌种可以防治地下害虫以及玉米土传病害，提高玉米种子的抗虫抗病能力，同时玉米拌种剂中含有营养成分，可以促进种子发芽，促进玉米根系的生长，使玉米苗期苗齐苗壮，为玉米高产奠定非常好的基础。播种深度，一般建议是3-5cm即可，播种过浅或者深都会影响玉米出苗。玉米是喜光作物，密度太大，玉米后期导致透风不良，湿度大，病虫害严重，导致玉米产量降低。', 
        '棉花':'一般以5cm地温稳定通过16C时播种为宜，新疆棉花种植时间约为4月20日左右。栽培的棉田，建议亩密度在2000~2500株，采用100cm左右宽行等行种植。', 
        '芝麻':'芝麻相对比较耐旱，耐涝性比较差，因此，选择的土地最好是地势高燥，土壤中等肥力以上，遇到大雨不发生渍害。芝麻比较耐贫瘠，要想获得高产，还需要一定的肥力条件，尽量不重茬种植。芝麻喜光，喜温暖，经种植经验表明，地势高燥的肥沃的沙质土地，由于透气性比较好，如果再配合水浇条件，芝麻很容易获得高产。芝麻种子比较小，对土地平整度，有一定的要求，土壤中不能有大的坷垃。', 
        '洋芋':'选择土壤肥沃、地势平坦、排水良好、耕层深厚且疏松的砂壤土。选择表皮光滑、色泽鲜美、重量1-2两左右的健康种薯作种，种薯切块前，建议将种薯放在阳光下晾晒2-3天，且切块刀具要进行消毒处理，避免病菌感染种薯，种薯切块不宜过大或过小，尽量用种薯的顶芽，少用底部的芽，这样可以保证马铃薯出苗率，提高马铃薯产量。', 
        '小麦':'小麦的根系主要分布区在20~40厘米，建议施肥水施到这个周围比较合适一些。一般建议每亩40方到50方左右就可以，如果有喷灌条件可以适当再低一点，尽量用小水灌溉，因为水大了以后，一旦上冻，反而容易伤根。', 
        '番茄':'（1）温度：番茄生长的最佳温度为24-26度，低于5度或高于40度时番茄会停止生长，所以我们要适时控制温度，特别是设施栽培。 （2）光照：番茄是喜光作物，对光照反应特别敏感。 光照充足的情况下，植株的长势会比较旺盛，抗病性也比较强；反之光照弱就会徒长，落花落果严重，从而降低来坐果率和产量。', 
        '大蒜':'种植大蒜，一般建议沟深度为5厘米，然后盖上2公分比较合适，还有就是秋季种植的大蒜，在为了在入冬前，长到一定的高度，才能安全过冬，栽植的时候可以再深一些，让根系更好的吸收养分，中耕时再适当清土，覆膜大蒜种植除外。', 
        '姜':'平摆法，即将姜块水平放在沟内. 使姜芽方向保持一致，东西向沟，姜芽一律向南南北向沟畦，姜芽一律向西摆放。 种姜摆放好后，用手轻轻按人泥中，使姜芽与土面相平，再用手从姜垄中下部扒些湿润细土盖住姜芽，以免烈日晒伤幼芽。 此法便于取老姜，应用居多。', 
        '李子':'花前施肥可以让花芽饱满，枝叶快速伸展；壮果肥在果实膨大时施肥，促进果实膨大；采果肥在李子采摘后施肥，养护果树，保证来年花芽饱满。', 
        '荸荠':'合理管水：荸荠苗定植后，最好保持2-3厘米浅水层稳苗，封行后深水控蘖分株，提早结荠，促球茎增多增大，球茎膨大期，切忌缺水。科学施肥：种植荸荠一定要氮、磷、钾三要素配合，切忌偏施、重施氮肥，补充硼、锌、锰等微量元素。', 
        '椪柑':'种植椪柑的土壤应是偏酸性或者中性的，还要足够的肥沃。最好种植在年平均气温在15℃以上的地方，建议种植在室外或者阳台。', 
        '梨':'一般建议选择肥沃情况良好、靠近水源、排水和灌溉方便的沙质壤土比较好，香梨的栽种我们可以采用穴垦的方式进行整地，这样可以减少种植的工作量，然后施入充足的基肥。 一般建议选择粗壮的、健康、没有病虫害损害的、根系发达没有伤害的苗木进行种植，如果是嫁接的话，建议选用一两年生的、粗壮的苗木即可进行嫁接。', 
        '枇杷':'枇杷种子发芽的适宜温度是在20℃～25℃。枇杷树的适应能力很强的，对土壤的要求也不太高，既能耐旱，也能耐热，在栽种以后管理起来也方便，只要注意浇水、施肥、光照和温度，并结合适当的修剪和防虫，那一般产量都不低的。', 
        '猕猴桃':'猕猴桃害怕温度高，特别干旱的地方然后枝叶也不适应，太冷的地方，否则会被冻的枯萎，所以，猕猴桃种植要选择那些温度高，但是环境比较湿润的地方，在海拔一千米左右开始种植比较好。', 
        '茶油':'茶油树不适宜在干旱的环境中发育，油茶地的地形、坡向也直接影响到茶油树的生长。', 
        '稻谷':'水稻的生长过程中需水量很大，适宜种植在高温多雨的地区。',  
        '豆皮':'暂无', 
        '竹笋':'种植竹笋后要保持土壤湿润，如果天气干旱之前需要每两到三天就浇水一次，如果遇到雨天，要提前做好防洪排涝工作，发现病虫害及时防治。竹笋种植后的施肥。因为竹笋的产量很高，因此它的生长就需要大量的肥料。', 
        '竹荪':'竹荪菌丝体生长以15-22度较为宜，26度以上生长缓慢乃至完全停止生长。子实体在15-28度均可发生，但以20-24度较为适宜。竹荪是喜湿性菌类，子实体需要较高湿度下才能正常生长发育。竹荪在生长发育过程中，自始至终都需要微酸性的环境。', 
        '脚板薯':'脚板薯的种薯一般在50~100克之间，太大的尽量切开成小块。每年的三月份和四月份都是种植脚板薯的最佳时间。因此，底肥要以农家肥为主，化肥为辅的方案最好。', 
        '大豆':'大豆对磷肥的需求量更敏感，所以在播种前施底肥的时候保持1：2的氮素与磷素比例比较好。再比如说，在施好底肥的基础上，在花生和大豆生长过程中的追肥管理上，我们适当补充一些钼肥、钙肥、镁肥、硼肥等中微量元素肥料（建议叶面喷施使用），往往能够让花生和大豆获得更高的产量和更好的品质。', 
        '藕':'选择背风向阳，排灌方便，耕作层20－30厘米，有犁底层的肥沃田块作藕田。 池塘种藕要求水深不超过1米，水位较为稳定，有犁底层。', 
    }
    variety_purchase = {
        '大米':'优质大米色泽清白，有光泽，呈半透明状，米粒大小均匀、丰满光滑，很少有碎米、爆腰(米粒上有裂纹)、腹白(米粒上乳白色不透明部分叫腹白，是由于稻谷未成熟，糊精较多而缺乏蛋白质)，无虫，不含杂质。 次质、劣质大米的色泽呈白色或微淡黄色，透明度差或不透明，霉变的米粒表面是绿色、黄色、灰褐色、黑色等。', 
        '茶叶':'品评茶叶的好坏，不能片面地只从一个或某几个角度去鉴别，要视其外形、叶底和茶汤的色泽，尝其滋味，嗅其香气，最后才能给出一个相对客观的评价。', 
        '蜜柚':'圆一些的果肉会比较多，重一些的果肉丰满、汁水很多；按下去一点就觉得比较硬的话，那么代表里面的肉很多。藕的种植时间种植莲藕的适宜时间是每年的3-4月，适合莲藕生长的温度为20-30℃左右。', 
        '花生':'优质的花生米颗粒会很饱满，外表的红衣也光泽均匀，一般来说，外皮呈桃红色的质量会比较好。', 
        '玉米':'购买玉米的时候，那些带外皮是首选，不太建议购买没有外皮的玉米。储存的时候不能将玉米外皮全部掰掉，需要留下3层左右的外皮，能保证不露出玉米粒就够了。', 
        '棉花':'暂无', 
        '芝麻':'优质的黑芝麻粒大饱满，大小均匀。它通常一头圆一头尖，有网状纹，而且通常不会全部都呈黑色。', 
        '洋芋':'形状长得畸形的不要买，损坏破皮的不要买，3、表面太过于光滑干净的不要买，发芽的不要买', 
        '小麦':'要选择麦粒饱满、产量高、品质好的。', 
        '番茄':'挑选拿着比较重手的番茄，这样的番茄水分充足，尽量挑选捏着偏软的番茄。', 
        '大蒜':'一般的大蒜外皮是白色中带着一点紫色的或者全紫皮的，这样的大蒜比较优质，吃起来蒜香味十足，营养方面也比较高。大蒜的表皮如果发黑，就说明大蒜在存放的过程中没有保存好，表皮开始有些霉烂，这样的大蒜也是不适合购买的。', 
        '姜':'带有细嫩芽的生姜属于活姜，这样的生姜才是适合购买的，不管是营养水分还是新鲜度，都是比较好的。如果是一丁点芽都没有的话，这样的生姜就属于死姜，也就是生姜已经缺乏活性，其内部营养水分流失都比较大。', 
        '李子':'买李子的时候，捏几下看看李子硬度。如果它们有弹性，呈深红色，一般来说，它们是完全成熟的甜李子。而且如果捏得很用力，而且表面呈半绿半黄的状态，一般来说还不够成熟，可能会有点酸味。有些人喜欢吃酸酸甜甜的未成熟的李子，依个人喜好而定，如果李子不成熟，存放几天后就会成熟。', 
        '荸荠':'选购荸荠最重要的是看其颜色、大小和硬度，荸荠以皮薄，肉白，质硬，无破损为佳。首先荸荠的颜色，以颜色紫红为佳，需要注意的是颜色浅且顶芽短，则汁多味甜，适合鲜食；颜色深一点且顶芽长的荸荠，甜味略淡，适合熟食。再者看大小，荸荠个大为好。最后用手捏一下硬度，质地硬，不软烂凹陷的是新鲜优质的荸荠。', 
        '椪柑':'从外观上来看，挑选果皮没有伤痕，颜色比较鲜活不暗红，表面光滑有亮泽度的，有些看起来很大的椪柑，果皮太厚，而且表面有突起的斑点。', 
        '梨':'梨茎为浅绿色，周围的梨肉比较饱满，表明该梨在采摘后已保存了很短的时间。该果肉具有足够的水分，高甜度，并且味道甜美可口。', 
        '枇杷':'我们在买枇杷的时候，不要只会挑大的，而是要挑选个头中等的枇杷，果核也是比较小的，如果个头太大的话，果核就比较大。而且我们也是需要注意它的形状和颜色的。要挑选那种椭圆的，并且是金黄颜色的，这样才是优质的枇杷。', 
        '猕猴桃':'猕猴桃是否新鲜一定要先看猕猴桃的颜色，一般市面上售卖的猕猴桃颜色大多是深色和绿色两种，很多人买猕猴桃都认为是深色的猕猴桃更成熟，所以买深色，其实不然，相反绿色的猕猴桃才是更为的成熟。', 
        '茶油':'首先是酸值，酸值越低越好，一般企业控制在1.0以内。 如果你购买的茶油放入手心摩擦或者锅内加热有酸味，那说明油品质量差，质量好的茶油即使加热超过200摄氏度也不可能有酸味。 然后是烟点，烟点越高，说明油品质量越高。', 
        '稻谷':'优质大米色泽清白，有光泽，呈半透明状，米粒大小均匀、丰满光滑，很少有碎米、爆腰(米粒上有裂纹)、腹白(米粒上乳白色不透明部分叫腹白，是由于稻谷未成熟，糊精较多而缺乏蛋白质)，无虫，不含杂质。 次质、劣质大米的色泽呈白色或微淡黄色，透明度差或不透明，霉变的米粒表面是绿色、黄色、灰褐色、黑色等。', 
        '豆皮':'上好的豆腐皮有一股淡淡的豆香味，不可能有酸味。 如果豆腐皮的颜色暗黄，每片都薄厚不均，说明质量比较差，不宜购买。 质量好的豆腐皮，透明色泽微黄，柔软富有弹性。 豆腐皮无论薄厚都要有一定韧性，如果一拉就碎，则韧性不足，说明质量比较差。', 
        '竹笋':'如果笋壳是嫩黄色的，说明里面的竹笋是比较嫩的，因为没有完全出土和刚出土的竹笋壳通常都是黄色的。', 
        '竹荪':'挑选竹荪时，要注意颜色偏黄的，这种竹荪是自然烘烤而成的，自然醇香，味道清甜。 颜色过白的可能是用硫磺熏过的劣质竹荪，闻起来味道刺鼻，口感酸涩，不宜选购。 第二，看大小。 挑选竹荪时应挑选朵大肉厚，朵小肉薄的多为“营养不良”型。', 
        '大豆':'新鲜的黄豆色泽明亮有光泽，陈旧的黄豆颜色不鲜艳，像褪了色的。', 
        '脚板薯':'一般来说外表干净、光滑、形状好,脚板薯比较坚硬而且外皮发亮的话,说明是新鲜的;若是脚板薯不仅发芽了,而且表面凹凸不平的话,这类红薯是不新鲜的,不建议购买。', 
        '藕':'藕节粗且短、间距长，带有湿泥土，莲藕要外形饱满，不要选择外型凹凸不完整的莲藕。', 
    }
    #种植建议
    if variety in variety_advice:
        result['plant_advices'] = [{'advice': variety_advice[variety]}]
    else:
        result['plant_advices'] = [
            {
                'advice': '暂无'
            }
        ]

    #购买建议
    if variety in variety_purchase:
        result['purchase_advices'] = [{'advice': variety_purchase[variety]}]
    else:
        result['purchase_advices'] = [
            {
                'advice': '暂无'
            }
        ]

def get_variaty_text(result, variety):
    # varietyList:['价格','品质','色泽','口感','包装','分量','物流','售后'],
    comment_dict = {
        '价格': ['便宜', '中等', '较高'],
        '品质': ['较好', '中等', '较差'],
        '色泽': ['较好', '中等', '不佳'],
        '口感': ['较好', '中等', '较差'],
        '包装': ['精美', '中等', '不够精美'],
        '分量': ['较多', '中等', '较少'],
        '物流': ['较好', '中等', '较差'],
        '售后': ['服务较好', '服务中等', '服务较差'],
        '其他': ['方面较好', '方面中等', '方面较差'],
    }
    text = '总体来说，这段时间内' + variety
    aspect_texts = []
    aspect_comments = {}
    for item in result['aspect_details']:
        aspect = item['aspect']
        score = 0
        for i in item['sentiment_distribution']:
            if i['sentiment'] == '正面':
                score += i['percent']
            elif i['sentiment'] == '负面':
                score -= i['percent']
        if score > 0.4:
            aspect_texts.append(aspect + comment_dict[aspect][0])
            aspect_comments[aspect] = '满意'
        elif score < -0.4:
            aspect_texts.append(aspect + comment_dict[aspect][2])
            aspect_comments[aspect] = '不满意'
        else:
            aspect_texts.append(aspect + comment_dict[aspect][1])
            aspect_comments[aspect] = '一般'
        if aspect == '其他':
            aspect_texts.pop()
    text = text + '，'.join(aspect_texts) + '。'
    print(text)
    result['aspect_text'] = text
    result['aspect_comments'] = aspect_comments

@api.route('/getSentimentAnalysis', methods=['POST'])
def get_sentiment_analysis():
    if request.is_json:
        location = request.get_json()["location"]
        variety = request.get_json()["variety"]
        start_date = request.get_json()["start_date"]
        end_date = request.get_json()["end_date"]
        print('Received json: ', location, variety, start_date, end_date)
    elif hasattr(request, 'args'):
        location= request.args.get("location")
        variety = request.args.get("variety")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        print('Received args: ', location, variety, start_date, end_date)
    else:
        print(type(request))
        return

    result = {}
    result['daily_info'] = EVENT.get_daily_info(location, variety, start_date, end_date)
    result['daily_info'] = sorted(result['daily_info'], key=lambda x: x["date"], reverse=False)

    data_list = EVENT.get_date_info(location, variety, start_date, end_date)
    if data_list == None or len(data_list) == 0:
        return {'code':200, 'msg':'查询无结果', 'data':{}}
    
    # 评分分布
    score_dict = {}
    for data in data_list:
        if data['user_star'] in score_dict:
            score_dict[data['user_star']].append(data)
        else:
            score_dict[data['user_star']] = [data]
    result['score_distribution'] = []
    total_score = 0
    total_number = 0
    for key in score_dict:
        temp = {}
        temp['score'] = int(key)
        temp['number'] = len(score_dict[key])
        temp['percent'] = float(temp['number'])/len(data_list)
        result['score_distribution'].append(temp)
        total_score += temp['score'] * temp['number']
        total_number += temp['number']
    result['score_distribution'] = sorted(result['score_distribution'], key=lambda x: x["score"], reverse=False)
    
    # 概览文本
    avg_score = total_score / total_number
    date_period = datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')
    avg_heat = total_number / date_period.days
    get_info_text(result, variety, avg_score, avg_heat)
    get_fixed_advice(result, variety)

    #属性分布
    analysisResult = EVENTMODEL.txt_analysis(data_list)
    result['aspect_distribution'] = []
    temp_sum_count = sum([x['count'] for x in analysisResult['statistics_result']['variety'][variety]['aspect'].values()])
    for key in analysisResult['statistics_result']['variety'][variety]['aspect']:
        temp = {}
        temp['aspect'] = key
        temp['number'] = analysisResult['statistics_result']['variety'][variety]['aspect'][key]['count']
        temp['percent'] = float(temp['number'])/temp_sum_count
        result['aspect_distribution'].append(temp)
    result['aspect_distribution'] = sorted(result['aspect_distribution'], key=lambda x: x["aspect"], reverse=False)
    
    #情感分布
    pos_dict = {}
    neg_dict = {}
    summary_dict= {}
    result['aspect_details'] = []
    for key in analysisResult['statistics_result']['variety'][variety]['aspect']:
        temp = {}
        temp['aspect'] = key
        temp['sentiment_distribution'] = [
            {'sentiment':'正面', 'number':0, 'percent': 0},
            {'sentiment':'负面', 'number':0, 'percent': 0},
            {'sentiment':'中性', 'number':0, 'percent': 0}
        ]
        temp_sum_count = sum([x for x in analysisResult['statistics_result']['variety'][variety]['aspect'][key]['polarity'].values()])
        for pos in analysisResult['statistics_result']['variety'][variety]['aspect'][key]['polarity']:
            if pos == 'POS':
                temp['sentiment_distribution'][0]['number'] = analysisResult['statistics_result']['variety'][variety]['aspect'][key]['polarity'][pos]
                temp['sentiment_distribution'][0]['percent'] = float(analysisResult['statistics_result']['variety'][variety]['aspect'][key]['polarity'][pos])/temp_sum_count
            if pos == 'NEG':
                temp['sentiment_distribution'][1]['number'] = analysisResult['statistics_result']['variety'][variety]['aspect'][key]['polarity'][pos]
                temp['sentiment_distribution'][1]['percent'] = float(analysisResult['statistics_result']['variety'][variety]['aspect'][key]['polarity'][pos])/temp_sum_count
            if pos == 'NEU':
                temp['sentiment_distribution'][2]['number'] = analysisResult['statistics_result']['variety'][variety]['aspect'][key]['polarity'][pos]
                temp['sentiment_distribution'][2]['percent'] = float(analysisResult['statistics_result']['variety'][variety]['aspect'][key]['polarity'][pos])/temp_sum_count
        
        #评价关系对相关
        target_dict = {}
        opinion_dict ={}
        units_dict= {'POS':[], 'NEG':[], 'NEU':[]}
        opinion_sent_dict = {'POS':{}, 'NEG':{}, 'NEU':{}}
        for target_value in analysisResult['statistics_result']['variety'][variety]['aspect'][key]['target']:
            if target_value not in target_dict:
                target_dict[target_value] = analysisResult['statistics_result']['variety'][variety]['aspect'][key]['target'][target_value]['count']
            else:
                target_dict[target_value] += analysisResult['statistics_result']['variety'][variety]['aspect'][key]['target'][target_value]['count']
            for opinion_value in analysisResult['statistics_result']['variety'][variety]['aspect'][key]['target'][target_value]['opinion']:
                if opinion_value not in opinion_dict:
                    opinion_dict[opinion_value] = analysisResult['statistics_result']['variety'][variety]['aspect'][key]['target'][target_value]['opinion'][opinion_value]['count']
                else:
                    opinion_dict[opinion_value] += analysisResult['statistics_result']['variety'][variety]['aspect'][key]['target'][target_value]['opinion'][opinion_value]['count']
                for pos_value in analysisResult['statistics_result']['variety'][variety]['aspect'][key]['target'][target_value]['opinion'][opinion_value]['polarity']:
                    units_dict[pos_value].append([{'target':target_value, 'opinion': opinion_value}, analysisResult['statistics_result']['variety'][variety]['aspect'][key]['target'][target_value]['opinion'][opinion_value]['polarity'][pos_value]])
                    if opinion_value not in opinion_sent_dict[pos_value]:
                        opinion_sent_dict[pos_value][opinion_value] = 1
                    else:
                        opinion_sent_dict[pos_value][opinion_value] += 1

        ##更新总评价dict
        pos_dict = dict(Counter(pos_dict) + Counter(opinion_sent_dict['POS']))
        neg_dict = dict(Counter(neg_dict) + Counter(opinion_sent_dict['NEG']))
        summary_dict = dict(Counter(summary_dict) + Counter(opinion_dict))
        
        target_list = list(zip(list(target_dict.keys()), list(target_dict.values())))#.sort(key = lambda x :x[1], reverse = True)
        opinion_list = list(zip(list(opinion_dict.keys()), list(opinion_dict.values())))#.sort(key = lambda x :x[1], reverse = True)

        #对象分布
        target_list.sort(key = lambda x :x[1], reverse = True)
        temp_sum_count = sum([x[1] for x in target_list])

        ##过滤None
        target_list = list(filter(lambda x: x[0] != 'NONE', target_list))

        if len(target_list) > 20:
            target_list = target_list[:20]
        for i, element in enumerate(target_list):
            target_list[i] = {'target': element[0], 'number': element[1], 'percent':float(element[1])/temp_sum_count}
        temp['target_distribution'] = target_list

        #观点分布
        opinion_list.sort(key = lambda x :x[1], reverse = True)
        temp_sum_count = sum([x[1] for x in opinion_list])

        ##过滤None
        opinion_list = list(filter(lambda x: x[0] != 'NONE', opinion_list))

        if len(opinion_list) > 20:
            opinion_list = opinion_list[:20]
        for i, element in enumerate(opinion_list):
            opinion_list[i] = {'opinion': element[0], 'number': element[1], 'percent':float(element[1])/temp_sum_count}
        temp['opinion_distribution'] = opinion_list

        #正面评价
        units_dict['POS'] = sorted(units_dict['POS'], key = lambda x: x[1], reverse = True)[:50]
        temp['positive_units'] = [{'target': x[0]['target'], 'opinion': x[0]['opinion'], 'times': x[1]} for x in units_dict['POS']]

        #负面评价
        units_dict['NEG'] = sorted(units_dict['NEG'], key = lambda x: x[1], reverse = True)[:50]
        temp['negative_units'] = [{'target': x[0]['target'], 'opinion': x[0]['opinion'], 'times': x[1]} for x in units_dict['NEG']]

        #中性评价
        units_dict['NEU'] = sorted(units_dict['NEU'], key = lambda x: x[1], reverse = True)[:50]
        temp['neutral_units'] = [{'target': x[0]['target'], 'opinion': x[0]['opinion'], 'times': x[1]} for x in units_dict['NEU']]
        
        result['aspect_details'].append(temp)

    result['aspect_details'] = sorted(result['aspect_details'], key=lambda x: x["aspect"], reverse=False)
    
    get_variaty_text(result, variety)

    return jsonify({'code':200, 'msg':'查询成功', 'data':result})
