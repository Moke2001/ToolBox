from Framework.Format.ModelFormat.ModelFormat import ModelFormat
from Framework.QutipBox.ModelQutip.ModelQutip import ModelQutip
from Framework.TenpyBox.ModelTenpy.ModelTenpy import ModelTenpy


def model_translator(model,type):
    if type == "qutip":
        if isinstance(model, ModelFormat):
            if isinstance(model,ModelQutip):
                return model
            else:
                return ModelQutip(model)
        else:
            raise TypeError("参数model必须是ModelFormat对象")
    elif type=='tenpy':
        if isinstance(model, ModelFormat):
            if isinstance(model,ModelTenpy):
                return model
            else:
                return ModelTenpy(model)
        else:
            raise TypeError("参数model必须是ModelFormat对象")
    elif type=='format':
        if isinstance(model, ModelTenpy) or isinstance(model,ModelQutip):
            return ModelFormat(model)
        elif isinstance(model,ModelQutip):
            return model
