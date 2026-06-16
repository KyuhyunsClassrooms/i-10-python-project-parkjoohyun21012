# AI 활용 자유 주제 파이썬 미니 프로젝트
# 이름 또는 학번: 21012 박주현
# 프로젝트 주제: 전기차/ESS 배터리 팩 관리 및 수명 진단 시스템 (BMS 시뮬레이터)

#여러 배터리 팩의 잔량(SOC)과 건강도(SOH)를 계산하고
# 상태를 정상/주의/위험으로 진단하는 BMS 시뮬레이터입니다



# ------------------------------------------------------------
# 1. 데이터 준비: 2차원 리스트
# ------------------------------------------------------------
# 현재 열의 의미:
# 0번 열: 팩 ID
# 1번 열: 소재 종류 (LFP, NCM, 전고체)
# 2번 열: 설계 용량 (Ah)
# 3번 열: 현재 잔량 (Ah)
# 4번 열: 누적 사이클 수
# 5번 열: 최대 사이클 수명
# ------------------------------------------------------------
 
battery_packs = [
    ["PACK-01", "LFP",    100, 87,  320, 3000],
    ["PACK-02", "NCM",    120, 45,  810, 1500],
    ["PACK-03", "전고체",  90, 91,   55, 5000],
    ["PACK-04", "LFP",   100,  8,  2890, 3000],
    ["PACK-05", "NCM",   120, 110,  430, 1500],
]
 
# 열 인덱스 상수
ID      = 0
MAT     = 1
CAP_MAX = 2
CAP_NOW = 3
CYCLES  = 4
MAX_CYC = 5
 
 
# ------------------------------------------------------------
# 2. 함수 정의
# ------------------------------------------------------------
 
def show_intro():
    """프로그램 제목과 등록된 팩 수를 출력한다."""
    print("=" * 62)
    print("  전기차/ESS 배터리 팩 관리 및 수명 진단 시스템 (BMS)")
    print("=" * 62)
    print(f"  등록된 배터리 팩 수: {len(battery_packs)}개")
 
 
def calculate_soc(pack):
    """SOC(배터리 잔량 %)를 계산해 반환한다."""
    soc = (pack[CAP_NOW] / pack[CAP_MAX]) * 100
    return round(soc, 1)
 
 
def calculate_soh(pack):
    """SOH(배터리 건강도 %)를 사이클 기반으로 계산해 반환한다."""
    soh = (1 - pack[CYCLES] / pack[MAX_CYC]) * 100
    if soh < 0:
        soh = 0
    return round(soh, 1)
 
 
def diagnose_pack(pack):
    """SOC·SOH를 계산하고 상태(정상/주의/위험)와 경고 메시지를 반환한다."""
    soc = calculate_soc(pack)
    soh = calculate_soh(pack)
    warnings = []
    status = "정상"
 
    # 조건문: SOC 기준 상태 판정
    if soc > 100:
        warnings.append("과충전 감지 (SOC > 100%)")
        status = "위험"
    elif soc < 10:
        warnings.append("과방전 위험 (SOC < 10%)")
        status = "위험"
    elif soc < 20:
        warnings.append("잔량 부족 (SOC < 20%)")
        status = "주의"
 
    # 조건문: SOH 기준 상태 판정
    if soh < 20:
        warnings.append("배터리 수명 임박 (SOH < 20%)")
        if status != "위험":
            status = "위험"
    elif soh < 50:
        warnings.append("배터리 노화 진행 (SOH < 50%)")
        if status == "정상":
            status = "주의"
 
    if not warnings:
        warnings.append("이상 없음")
 
    return soc, soh, status, warnings
 
 
def print_report(packs):
    """모든 배터리 팩의 진단 결과를 표 형식으로 출력한다."""
    print("\n" + "=" * 62)
    print("     BMS 배터리 팩 진단 리포트")
    print("=" * 62)
    print(f"{'팩ID':<10} {'소재':<8} {'SOC':>6} {'SOH':>6} {'상태':>6}")
    print("-" * 62)
 
    # 반복문: 2차원 리스트의 모든 팩을 순회하며 진단
    for pack in packs:
        soc, soh, status, warnings = diagnose_pack(pack)
        print(f"{pack[ID]:<10} {pack[MAT]:<8} {soc:>5}% {soh:>5}% {status:>6}")
        for w in warnings:
            if w != "이상 없음":
                print(f"           └ {w}")
 
    print("-" * 62)
 
    total   = len(packs)
    danger  = sum(1 for p in packs if diagnose_pack(p)[2] == "위험")
    caution = sum(1 for p in packs if diagnose_pack(p)[2] == "주의")
    normal  = total - danger - caution
    danger_ids = [p[ID] for p in packs if diagnose_pack(p)[2] == "위험"]
 
    print(f"\n[전체 요약]  총 {total}팩  |  정상 {normal}  주의 {caution}  위험 {danger}")
    if danger_ids:
        print(f"즉시 점검 필요 팩: {', '.join(danger_ids)}")
    print("=" * 62)
 
 
def get_user_input():
    """상세 진단할 팩 ID를 입력받는다. (전체: 0, 종료: q)"""
    print("\n상세 진단할 팩 ID를 입력하세요. (전체 보기: 0 / 종료: q)")
    ids = [p[ID] for p in battery_packs]
 
    # 반복문: 올바른 입력이 들어올 때까지 반복
    while True:
        choice = input("입력: ").strip().upper()
        if choice == "Q":
            return None
        if choice == "0":
            return "ALL"
        if choice in ids:
            return choice
        print(f"  [오류] 올바른 팩 ID를 입력하세요. {ids}")
 
 
def print_detail(pack_id):
    """특정 팩의 상세 진단 결과를 출력한다."""
    for pack in battery_packs:
        if pack[ID] == pack_id:
            soc, soh, status, warnings = diagnose_pack(pack)
            remaining = pack[MAX_CYC] - pack[CYCLES]
            print(f"\n[{pack[ID]} 상세 진단]")
            print(f"  소재          : {pack[MAT]}")
            print(f"  설계 용량     : {pack[CAP_MAX]} Ah")
            print(f"  현재 잔량     : {pack[CAP_NOW]} Ah")
            print(f"  SOC (잔량%)   : {soc}%")
            print(f"  누적 사이클   : {pack[CYCLES]}회")
            print(f"  잔여 사이클   : {remaining}회")
            print(f"  SOH (건강도)  : {soh}%")
            print(f"  현재 상태     : [{status}]")
            print(f"  진단 메시지   :")
            for w in warnings:
                print(f"    - {w}")
            return
    print("  해당 팩을 찾을 수 없습니다.")
 
 
def main():
    show_intro()
    print_report(battery_packs)
 
    while True:
        choice = get_user_input()
        if choice is None:
            print("\n프로그램을 종료합니다.")
            break
        elif choice == "ALL":
            print_report(battery_packs)
        else:
            print_detail(choice)
 
 
# ------------------------------------------------------------
# 3. 프로그램 실행
# ------------------------------------------------------------
main()