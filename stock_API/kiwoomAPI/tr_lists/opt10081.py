from pandas import DataFrame


def opt10081_out(trcode, record_name, get_comm_data, get_repeat_cnt):
    """주식 일봉차트 조회 요청"""

    data_cnt = get_repeat_cnt(trcode, record_name)
    ohlcv = {"date": [], "open": [], "high": [], "low": [], "close": [], "volume": []}

    for i in range(data_cnt):
        date = get_comm_data(trcode, record_name, i, "일자")
        open_P = get_comm_data(trcode, record_name, i, "시가")
        high_P = get_comm_data(trcode, record_name, i, "고가")
        low_P = get_comm_data(trcode, record_name, i, "저가")
        close_P = get_comm_data(trcode, record_name, i, "현재가")
        volume = get_comm_data(trcode, record_name, i, "거래량")

        ohlcv["date"].append(date)
        ohlcv["open"].append(int(open_P))
        ohlcv["high"].append(int(high_P))
        ohlcv["low"].append(int(low_P))
        ohlcv["close"].append(int(close_P))
        ohlcv["volume"].append(int(volume))

    ret = DataFrame(ohlcv, columns=["date", "open", "high", "low", "close", "volume"])

    return ret


def opt10081_in(set_input_value, comm_rq_data, code: str, first_date: str = "20160101", adjustedClosingPrice: int = 1):
    """주식 일봉차트 조회 설정"""

    set_input_value("종목코드", code)
    set_input_value("기준일자", first_date)
    set_input_value("수정주가구분", str(adjustedClosingPrice))
    comm_rq_data("opt10081_req", "opt10081", 0, "2081")
