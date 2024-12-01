##---Create specific lattice in Qutip---##
from QutipToolBox.Lattice.Lattice import Lattice
from QutipToolBox.Site.Site import Site


def lattice_creator(lattice_parameter):
    L_x=lattice_parameter.get('L_x',1)
    L_y=lattice_parameter.get('L_y',1)
    L_z=lattice_parameter.get('L_z',1)
    a_x=lattice_parameter.get('a_x',1)
    a_y=lattice_parameter.get('a_y',1)
    a_z=lattice_parameter.get('a_z',1)
    name=lattice_parameter.get('name',None)
    dimension=lattice_parameter.get('dimension',2)
    ##  正方晶格
    if name is 'Square':
        site_list=[]
        for i in range(L_x):
            for j in range(L_y):
                for k in range(L_z):
                    if L_z==1:
                        if L_y==1:
                            site_list.append(Site((a_x*i,),dimension))
                        else:
                            site_list.append(Site((a_x*i,a_y*j),dimension))
                    else:
                        site_list.append(Site((a_x*i,a_y*j,a_z*k),dimension))
        return Lattice(site_list)

    ##  抛出类型错误
    else:
        raise ValueError('There is no such type of lattice')