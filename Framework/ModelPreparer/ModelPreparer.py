from Framework.ModelPreparer.ModelTranslator import model_translator


def model_preparer(model,type):
    if type=='qutip' or type=='tenpy':
        model_result=model_translator(model,type)
        model_result.build()
        return model_result
    else:
        raise NotImplemented('参数type指定的只能是qutip或tenpy')

