##---Class Lattice in Qutip---##


class Lattice:
    ##  Lattice构造函数，包含一个Site list
    def __init__(self, site_list):
        assert isinstance(site_list, list),'site_list should be a list'
        self.site_list = site_list
        self.site_number=len(site_list)

    ##  获取Site list
    def get_site_list(self):
        return self.site_list

    ##  获取Site个数
    def get_site_number(self):
        return self.site_number

    ##  按照坐标或index获得Site对象
    def get_site(self, flag):
        if isinstance(flag, int):
            return self.site_list[flag]
        elif isinstance(flag, tuple):
            for i in range(self.site_number):
                if self.site_list[i].location == flag:
                    return self.site_list[i]

    ##  按照坐标或index获得Site index
    def get_site_index(self, flag):
        if isinstance(flag, int):
            return flag
        elif isinstance(flag, tuple):
            for i in range(self.site_number):
                if self.site_list[i].location == flag:
                    return i
