
typedef struct a
{
  int a;
}a;

typedef struct v
{
  int v;
}v;

void	*new()
{
  v *test = (v *) malloc(sizeof(struct a) + sizeof(struct v));
  test->v = 5;
  return test + sizeof(struct v);
}

void	delete(struct name *obj)
{
  void *fr = (void*)(obj - sizeof(struct v));
  free(fr);
}

int	main()
{
  a *x = new();
  x->a = 18;
  v *t = (v *) (x - sizeof(struct v));
  printf("%i\n", t->v);
  return 0;
}
