
class Stub(object):
    def __getattribute__(self,*args,**kwargs):
       if args[0] not in ('__class__','implemented_by') and not hasattr(self,'implemented_by'):
           f=open('pending_stubs.txt','a')
           f.write(self.__class__.__name__+':'+str(args[0])+'\n')
           f.close()
       return object.__getattribute__(self,*args,**kwargs)

class TestStub(Stub):
    test='hola'


if __name__=='__main__':
    t=TestStub()
    print t.test
