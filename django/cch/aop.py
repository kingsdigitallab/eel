# $Id$
'''
@summary: Aspect Oriented Programming Package. This lets you hook your own function in between other calls.
@author: geoffroy.noel@kcl.ac.uk
'''

def execute_before(cls, ori_mth_name,  pre_mth):
    ''' After calling this function, [pre_mth] will be automatically called before any instance call to [cls].[ori_mth_name]
        e.g. execute_before(AClass, 'amethod', myfunction)
    '''
    ori_mth = getattr(cls, ori_mth_name)
    def wrapper(*args, **kwargs):
        pre_mth(*args, **kwargs)
        return ori_mth(*args, **kwargs)
    setattr(cls, ori_mth_name, wrapper)
