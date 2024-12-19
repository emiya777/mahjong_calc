import yaml
import copy

from mahjongDef import *


def init_members(members):
    name2member_obj = {}
    for member in members:
        member_obj = Member(**member)
        name2member_obj[member['name']] = member_obj
    return name2member_obj



def calc_win(gameinfo, name2member_obj, pay_info_t): 
    result = gameinfo['result']
    who_win = result['who_win']
    who_win_obj = name2member_obj[who_win]
    win_type = result['win_type']
    
    base_point = gameinfo['WIN_POINT']
    odds = result['odds'] # 倍率
    final_point = odds * base_point
    
    who_lose = result['who_lose']
    who_lose_obj = name2member_obj.get(who_lose, None)
    
    if win_type == CHU_CHONG:
        info = {'from_': who_lose_obj, 'to_': who_win_obj, 'point': final_point, 'info': 'CHU_CHONG'}
        pay_info = PayInfo(**info)
        pay_info_t.append(pay_info)
    elif win_type == ZI_MO:
        for name, member_obj in name2member_obj.items():
            if is_same_member(name, who_win_obj): continue
            info = {'from_': member_obj, 'to_': who_win_obj, 'point': final_point, 'info': 'ZI_MO'}
            pay_info = PayInfo(**info)
            pay_info_t.append(pay_info)
            
    else:
        assert False, 'undefind win type'   
        
    
def calc_gangs(gameinfo, name2member_obj, pay_info_t):                  
    result = gameinfo['result']
    GANG_infos = result['GANG']
    base_point = gameinfo['GANG_POINT']
    base_point_AN = gameinfo['AN_GANG_POINT']
    
    if GANG_infos is None:
        return 
    
    for gang_info in GANG_infos:
        who_gang = gang_info['who_gang']
        who_gang_obj = name2member_obj[who_gang]
        
        if gang_info['type'] == GONG_GANG:
            for name, member_obj in name2member_obj.items():
                if is_same_member(name, who_gang_obj): continue
                info = {'from_': member_obj, 'to_': who_gang_obj, 'point': base_point, 'info': 'GONG_GANG'}
                pay_info = PayInfo(**info)
                pay_info_t.append(pay_info)
                
        elif gang_info['type'] == SI_GANG:
            gang_who = gang_info['gang_who']
            gang_who_obj = name2member_obj[gang_who]
            info = {'from_': gang_who_obj, 'to_': who_gang_obj, 'point': base_point*3, 'info': 'SI_GANG'}
            pay_info = PayInfo(**info)
            pay_info_t.append(pay_info)
            
        elif gang_info['type'] == AN_GANG:
            for name, member_obj in name2member_obj.items():
                if is_same_member(name, who_gang): continue
                
                info = {'from_': member_obj, 'to_': who_gang_obj, 'point': base_point_AN, 'info': 'AN_GANG'}
                pay_info = PayInfo(**info)
                pay_info_t.append(pay_info)
                
        else:
            assert False, 'undefind gang type' 
             

    

def horse_process(pay_info_t, gameinfo, name2member_obj):
    """
    计算中马
    """
    result = gameinfo['result']
    horses = result['horses']
    who_win = result['who_win'] 
    who_win_obj = name2member_obj[who_win]
    pay_info_t_by_house = []
    for horse in horses:
        for pay_info in pay_info_t:
            if is_same_member(pay_info.from_, horse):
                info = {
                    'info': copy.deepcopy(pay_info.info) + '(horse)',
                    'from_': who_win_obj,
                    'to_': pay_info.to_,
                    'point': pay_info.point
                    }  
                if is_same_member(info['from_'], info['to_']): continue
                
                pay_info = PayInfo(**info)
                pay_info_t_by_house.append(pay_info)
                
            elif is_same_member(pay_info.to_, horse):
                info = {
                    'info': copy.deepcopy(pay_info.info) + '(horse)',
                    'from_': pay_info.from_,
                    'to_': who_win_obj,
                    'point': pay_info.point
                    }  
                if is_same_member(info['from_'], info['to_']): continue
                
                pay_info = PayInfo(**info)
                pay_info_t_by_house.append(pay_info)
    
    pay_info_t += pay_info_t_by_house

def settle_pay_info_t(pay_info_t):
    for pay_info in pay_info_t:
        from_ = pay_info.from_
        to_ = pay_info.to_
        point = pay_info.point
        from_.point -= point    
        to_.point += point    
        print(pay_info) 
      
              
def mahjong_calc(gameinfo):
    pay_info_t = []
    name2member_obj = init_members(gameinfo['members'])
    
    calc_win(gameinfo, name2member_obj, pay_info_t)
    calc_gangs(gameinfo, name2member_obj, pay_info_t)
    
    horse_process(pay_info_t, gameinfo, name2member_obj)
    settle_pay_info_t(pay_info_t)
    
    print('\nsum:')    
    for member, member_obj in name2member_obj.items():
        s = f'{member_obj.name}: {member_obj.point}'    
        print(s)    
    print('end')