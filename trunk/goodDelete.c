void K_CM_MyClass_F_0void_0_delete(struct MyClass *self)
{
  void *fr = (void *) ( ((struct vtable_MyClass *)(self)) - 1);
    printf("delete : %p\n", fr);
    free(fr);
}
