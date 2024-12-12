from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.QutipBox.ModelQutip.ModelQutip import ModelQutip
from Framework.TenpyBox.ModelTenpy.ModelTenpy import ModelTenpy


def model_builder(model):
    if isinstance(model,ModelQutip) or isinstance(model,ModelTenpy):
        if not model.initial_check():
            model.build()
    else:
        raise TypeError('参数model必须是数据型Model对象')
