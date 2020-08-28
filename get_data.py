import requests
import json

def create_csv(file_name, json_data):
    """ data sample
    {"message":"success","result":[{"Code":"10000181","DiaLi":"7.50","GDCD":"7.00","HoaHoc":"","KHTN":"","KHXH":"6.58","LichSu":"5.25","ListGroup":[],"NgoaiNgu":"8.40","NguVan":"7.75","Result":null,"SinhHoc":"","Toan":"6.60","VatLi":""}]}
    """
    with open(file_name, 'a') as f:
        f.write('{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(json_data['Code'], json_data['DiaLi'], json_data['GDCD'], json_data['HoaHoc'], json_data['KHTN'], json_data['KHXH'], json_data['LichSu'], json_data['NgoaiNgu'], json_data['NguVan'], json_data['SinhHoc'], json_data['Toan'], json_data['VatLi']))

with requests.Session() as s:
    with open('cumthi.data', 'r', encoding='utf-8') as f:
        while 1:
            data = f.readline()
            if not data:
                break
            if 'Mã sở' in data:
                continue
            data_info = data.replace('\n', '').replace('\r', '').split('\t')
            sbd = 0
            while 1:
                code='{0:02d}'.format(int(data_info[2]))
                sbd_text = '{0:06d}'.format(sbd)
                url = 'https://diemthi.vnanet.vn/Home/SearchBySobaodanhFile?code={}{}&nam=2020'.format(code,sbd_text)
                p = s.get(url)
                print(p.text)
                sbd += 1
                result = json.loads(p.text)
                if (result['message'] != 'success'):
                    break

                if len(result['result']) == 0:
                    continue
                create_csv('{}_{}.csv'.format(data_info[1], data_info[2]), result['result'][0])
                