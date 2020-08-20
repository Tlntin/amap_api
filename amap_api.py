import requests
from pprint import pprint


class AMap(object):
    """
    高德地图sdk，编写时间2020-08-20
    作者邮箱：371043382@qq.com
    """
    def __init__(self, keys, sig=None, output="JSON"):
        """
        初始化，需要密钥
        :param keys: 密钥，需要去高德开放平台申请
        :param sig：数字签名,详见：https://lbs.amap.com/faq/quota-key/key/41169
        :param output: 输出，JSON or XML；设置 JSON 返回结果数据将会以JSON结构构成；如果设置 XML 返回结果数据将以 XML 结构构成。
        """
        self.keys = keys
        self.sig = sig
        self.output = output

    def get_data(self, url: str, params: dict):
        """
        获取基础数据
        :param url: 链接地址: Str类型
        :param params: 请求参数，Dict类型
        :return: 返回请求值
        """
        response = requests.get(url, params=params)
        data = False
        if response.status_code == 200:
            if self.output == 'JSON':
                data = response.json()
            else:
                data = response.text
        return data

    def location_encode(self, address, city=None, is_batch='false', callback=None):
        """
        地理位置转经纬度,官方文档参考：https://lbs.amap.com/api/webservice/guide/api/georegeo
        :param address: 国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦，如：北京市朝阳区阜通东大街6号。
                        如果需要解析多个地址的话，请用"|"进行间隔，并且将 batch 参数设置为 true，最多支持 10 个地址
                        进进行"|"分割形式的请求。
        :param city: 城市，Str类型，可以为中文也可以是拼音
        :param is_batch: 是否批量查询, Str类型，'true' or 'false'
        :param callback: 回调函数，值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效。
        :return status 返回结果状态值返回值为 0 或 1，0 表示请求失败；1 表示请求成功。
                count 返回结果数目
                info  返回状态说明，当 status 为 0 时，info 会返回具体错误原因，否则返回“OK”
                geocodes 地理编码信息列表，结果对象列表，包括下述字段：
                [
                    {
                        adcode：区域编码。例如：110101
                        building:建筑，Str类型，其为字典的Key，下面为其所对应的Value值
                        {
                            name: 建筑名称，List类型
                            type: 建筑类别，List类型
                         }
                        city：地址所在的城市名, Str类型。例如：北京市
                        citycode：城市编码，Str类型。例如:010
                        country: 国家，Str类型。国内地址默认返回中国
                        district：地址所在的区, Str类型。例如：朝阳区
                        formatted_address：结构化地址信息，Str类型。例如:省份＋城市＋区县＋城镇＋乡村＋街道＋门牌号码
                        level：匹配级别，Str类型
                        location：坐标点，Str类型。经度，纬度
                        neighborhood：社区信息，Dict类型
                        {
                            name: 社区名称，List类型。例如：['北京大学']
                            type：社区类型，List类型。例如：['科教文化服务','学校', '高等院校']
                        }
                        number：门牌，List类型。例如：例如：['6号']。
                        province：地址所在的省份名, Str类型。例如：'北京市'。此处需要注意的是，中国的四大直辖市也算作省级单位
                        street：街道，List类型。例如：['阜通东大街']
                        township：坐标点所在乡镇/街道（此街道为社区街道，不是道路信息），List类型。例如：['燕园街道']。
                    },
                    {...}
                ]
        """
        url = "https://restapi.amap.com/v3/geocode/geo?parameters"
        params = {
            'key': self.keys,
            'address': address,
            'city': city,
            'is_batch': is_batch,
            'sig': self.sig,
            'output': self.output,
            'callback': callback
        }
        data = self.get_data(url, params)
        return data

    def location_decode(self, location, poi_type=None, radius=1000, extensions="base", is_batch='false', road_level=None
                        , callback=None, home_or_corp=0):
        """
        该方法用于经纬度坐标转地理位置，官方文档参考：https://lbs.amap.com/api/webservice/guide/api/georegeo
        :param location: 经纬度坐标, Str类型。
                        传入内容规则：经度在前，纬度在后，经纬度间以“,”分割，经纬度小数点后不要超过 6 位。
                        如果需要解析多个经纬度的话，请用"|"进行间隔，并且将 batch 参数设置为 true，最多支持传入 20 对坐标点。
                        每对点坐标之间用"|"分割。
        :param poi_type: 以下内容需要 extensions 参数为 all 时才生效。
                        逆地理编码在进行坐标解析之后不仅可以返回地址描述，
                        也可以返回经纬度附近符合限定要求的POI内容（在 extensions 字段值为 all 时才会返回POI内容）。
                        设置 POI 类型参数相当于为上述操作限定要求。参数仅支持传入POI TYPECODE，可以传入多个POI TYPECODE，
                        相互之间用“|”分隔。该参数在 batch 取值为 true 时不生效。获取 POI TYPECODE 可以参考POI分类码表
        :param radius: 搜索半径， Int类型。radius取值范围在0~3000，默认是1000。单位：米
        :param extensions: Str类型，参数默认取值是 base，也就是返回基本地址信息；参数取值为 all 时会返回基本地址信息、附近 POI 内容、道路信息
                            以及道路交叉口信息。
        :param is_batch: 是否批量查询, Str类型，'true' or 'false'
        :param road_level: 以下内容需要 extensions 参数为 all 时才生效。可选值：0，1。
                            当road_level=0时，显示所有道路
                            当road_level=1时，过滤非主干道路，仅输出主干道路数据
        :param callback: callback值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效
        :param home_or_corp: 是否优化POI返回顺序
                            以下内容需要 extensions 参数为 all 时才生效。
                            home_or_corp 参数的设置可以影响召回 POI 内容的排序策略，目前提供三个可选参数：
                            0：不对召回的排序策略进行干扰。
                            1：综合大数据分析将居家相关的 POI 内容优先返回，即优化返回结果中 pois 字段的poi顺序。
                            2：综合大数据分析将公司相关的 POI 内容优先返回，即优化返回结果中 pois 字段的poi顺序。
        :return: status 返回结果状态值，Str类型。返回值为 0 或 1，0 表示请求失败；1 表示请求成功。
                 info 返回状态说明，Str类型。当 status 为 0 时，info 会返回具体错误原因，否则返回“OK”。
                      详情可以参考info状态表https://lbs.amap.com/api/webservice/guide/tools/info
                 regeocodes 逆地理编码,数据类型Dict或者List。
                            is_batch 字段设置为'true'时为批量请求，此时 regeocodes 标签返回，标签下为 regeocode对象列表；
                            is_batch 为'false'时为单个请求，会返回 regeocode 对象字典；
                            regeocode 对象包含的数据如下：
                 [/{
                    addressComponent: 地址元素字典
                    {
                        adcode: 行政区编码, Str类型。例如：110108。
                        building：楼信息，Dict类型
                        {
                            name: 建筑名称，List类型。例如：例如：['万达广场']
                            type: 建筑类型，List类型。例如：['科教文化服务', '学校', '高等院校']
                        }
                        businessAreas: 经纬度所属商圈，List类型
                        [
                            {
                            id: 商圈所在区域的adcode, Str类型。 例如: '440106'
                            location: 商圈中心点经纬度，Str类型。例如: '113.333776,23.119825'
                            name: 商圈名称, Str类型。例如：'珠江新城'
                            }，
                            {
                            ...
                            }
                        ]
                        city: 坐标点所在城市名称, Str类型。
                              请注意：当城市是省直辖县时返回为空，以及城市为北京、上海、天津、重庆四个直辖市时，该字段返回为空；
                              省直辖县列表，https://lbs.amap.com/faq/webservice/webservice-api/geocoding/43267
                        citycode: 城市编码，Str类型。例如：'010'
                        country: 国家，Str类型。国内地址默认返回中国
                        district：坐标点所在区，Str类型。例如：'海淀区'
                        neighborhood：社区信息，Dict类型
                        {
                            name: 社区名称，List类型。例如：['北京大学']
                            type：社区类型，List类型。例如：['科教文化服务','学校', '高等院校']
                        }
                        province: 坐标点所在省名称, Str类型。例如：北京市
                        streetNumber: 门牌信息, Dict类型
                        {
                            street: 街道名称。例如：中关村北二条
                            number: 门牌号。例如：3号
                            location: 坐标点。经纬度坐标点：经度，纬度
                            direction: 方向。坐标点所处街道方位。
                            distance: 门牌地址到请求坐标的距离。单位：米
                        }
                        towncode：乡镇街道编码，Str类型。例如：110101001000。
                        township：坐标点所在乡镇/街道（此街道为社区街道，不是道路信息），Str类型。例如：燕园街道。
                        seaArea: 所属海域信息。例如：渤海
                    }
                    formatted_address：结构化地址信息，Str类型。
                                      结构化地址信息包括：省份＋城市＋区县＋城镇＋乡村＋街道＋门牌号码。
                                      如果坐标点处于海域范围内，则结构化地址信息为：省份＋城市＋区县＋海域信息
                    roads: 道路信息列表。请求参数 extensions 为 all 时返回如下内容
                    [
                        road: 道路信息
                        [
                            id: 道路id
                            name: 道路名称
                            distance: 道路到请求坐标的距离。单位：米
                            direction: 方位。输入点和此路的相对方位
                            location: 坐标点
                        ]
                    ]
                    roadinters: 道路交叉口列表。请求参数 extensions 为 all 时返回如下内容。
                    [
                        roadinter: 道路交叉口
                        [
                            distance: 交叉路口到请求坐标的距离。	单位：米
                            direction: 方位。输入点相对路口的方位。
                            location: 路口经纬度
                            first_id: 第一条道路id
                            first_name: 第一条道路名称
                            second_id: 第二条道路id
                            second_name：第二条道路名称
                        ]
                    ]
                    pois: poi信息列表。请求参数 extensions 为 all 时返回如下内容
                    [
                        poi: poi信息列表
                        [
                            id: poi的id
                            name: poi点名称
                            type：poi类型
                            tel: 电话
                            distance: 该POI的中心点到请求坐标的距离。单位：米
                            direction: 方向。为输入点相对建筑物的方位
                            address: poi地址信息
                            location: 坐标点
                            businessarea: poi所在商圈名称
                        ]
                    ]
                    aois: aoi信息列表。请求参数 extensions 为 all 时返回如下内容
                    [
                        aoi: aoi信息
                        [
                            id: 所属 aoi的id
                            name: 所属 aoi 名称
                            adcode: 所属 aoi 所在区域编码
                            location: 所属 aoi 中心点坐标
                            area: 所属aoi点面积。单位：平方米
                            distance: 输入经纬度是否在aoi面之中。 0，代表在aoi内。其余整数代表距离AOI的距离
                        ]
                    ]
                 }/]
        """
        url = "https://restapi.amap.com/v3/geocode/regeo?parameters"
        params = {
            'key': self.keys,
            'location': location,
            'poi_type'.replace('_', ''): poi_type,
            'radius': radius,
            'extensions': extensions,
            'batch': is_batch,
            'road_level'.replace('_', ''): road_level,
            'sig': self.sig,
            'output': self.output,
            'callback': callback,
            'home_or_corp'.replace('_', ''): home_or_corp
        }
        data = self.get_data(url, params)
        return data

    def walking_path_plan(self, origin, destination, callback=None):
        """
        步行路径规划 API
        可以规划100KM以内的步行通勤方案，并且返回通勤方案的数据。
        官方文档参考地址：https://lbs.amap.com/api/webservice/guide/api/direction
        :param origin: 出发点, Str类型。需要提供经纬度
        :param destination: destination， Str类型。需要提供经纬度
        :param callback: callback值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效
        :return: status 返回结果状态值，Str类型。返回值为 0 或 1，0 表示请求失败；1 表示请求成功。
                 info 返回状态说明，Str类型。当 status 为 0 时，info 会返回具体错误原因，否则返回“OK”。
                      详情可以参考info状态表https://lbs.amap.com/api/webservice/guide/tools/info
                 count: 返回结果总数目, Str类型
                 route：路线信息，Dict类型
                 {
                    'origin': 起点坐标, Str类型
                    'destination': 终点坐标，Str类型
                    'paths': 步行方案, List类型
                    [
                        {
                            'distance': 起点和终点的步行距离, Str类型。单位米
                            'duration': 步行时间预计, Str类型，单位秒
                            'steps': 返回步行结果列表, List类型
                            [
                                {
                                    'instruction': 路段步行指示, Str类型
                                    'road': 道路名称，List类型
                                    'distance': 此路段距离，Str类型，单位米
                                    'orientation': 方向, Str类型
                                    'duration': 此路段预计步行时间, Str类型。单位秒
                                    'polyline': 此路段坐标点, Str类型
                                    'action': 步行主要动作,Str类型，
                                            详见https://lbs.amap.com/api/webservice/guide/api/direction#walk_action
                                    'assistant_action': 步行辅助动作, Str类型
                                            详见https://lbs.amap.com/api/webservice/guide/api/direction#walk_action
                                    'walk_type': 这段路是否存在特殊的方式, Str类型，具体参考代码如下：
                                                0，普通道路，1，人行横道，3，地下通道，4，过街天桥，5，地铁通道，6，公园
                                                7，广场，8，扶梯，9，直梯，10，索道，11，空中通道，12，建筑物穿越通道
                                                13，行人通道，14，游船路线，15，观光车路线，16，滑道
                                                18，扩路，19，道路附属连接线，20，阶梯
                                                21，斜坡，22，桥，23，隧道，30，轮渡
                                },
                                {...}
                            ]
                        },
                        {...}
                    ]
                 }
        """
        url = "https://restapi.amap.com/v3/direction/walking?parameters"
        params = {
            'key': self.keys,
            'sig': self.sig,
            'output': self.output,
            'origin': origin,
            'destination': destination,
            'callback': callback
        }
        data = self.get_data(url, params)
        return data

    def bus_path_plan(self, origin, destination, city, city_destination=None, extensions='base', strategy='0',
                      night_flag='0', date=0, time=0, callback=None):
        """
        公交路径规划 API 可以规划综合各类公共（火车、公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据。

        :param origin: 出发点，Str类型，经纬度
        :param destination: 目标地点，，Str类型，经纬度
        :param city: 城市/跨城规划时的起点城市，Str类型。目前支持市内公交换乘/跨城公交的起点城市，可选值：城市名称/citycode
        :param city_destination: 跨城公交规划时的终点城市，Str类型，跨域则必填。可选值：城市名称/citycode
        :param extensions: 返回结果详略，Str类型。可选值：base(default)/all。base:返回基本信息；all：返回全部信息
        :param strategy: 公交换乘策略，Str类型。可选值：0：最快捷；1：最经济；2：最少换乘；3：最少步行；5：不乘地铁模式
        :param night_flag: 是否计算夜班车。Str类型，可选值：0：不计算夜班车；1：计算夜班车。
        :param date: 出发日期，Str类型。例如：'2014-3-19'
        :param time: 出发时间, Str类型。例如：'22:34'
        :param callback: callback值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效
        :return: 具体自行查看：https://lbs.amap.com/api/webservice/guide/api/direction#bus
        """
        url = "	https://restapi.amap.com/v3/direction/transit/integrated?parameters"
        params = {
            'key': self.keys,
            'sig': self.sig,
            'output': self.output,
            'origin': origin,
            'destination': destination,
            'city': city,
            'city_d'.replace('_', ''): city_destination,
            'extensions': extensions,
            'strategy': strategy,
            'night_flag'.replace('_', ''): night_flag,
            'date': date,
            'time': time,
            'callback': callback
        }
        data = self.get_data(url, params)
        return data

    def bicycle_path_plan(self, origin, destination):
        """
        骑行路径规划用于规划骑行通勤方案，规划时不会考虑路况；考虑天桥、单行线、封路等情况。
        官方文档参考：https://lbs.amap.com/api/webservice/guide/api/direction#t8
        :param origin: 出发点，Str类型，经纬度
        :param destination: 目标地点，，Str类型，经纬度
        :return: 官方文档参考：https://lbs.amap.com/api/webservice/guide/api/direction#t8
        """
        url = "https://restapi.amap.com/v4/direction/bicycling?parameters"
        params = {
            'key': self.keys,
            'origin': origin,
            'destination': destination
        }
        data = self.get_data(url, params)
        return data
