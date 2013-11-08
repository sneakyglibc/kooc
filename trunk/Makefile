NAME		=	project_using_kooc

KOOC_SRCS	=	test.kc			\

KOOC_HDRS	=	module.kh		\

SRCS		=	$(KOOC_SRCS:.kc=.c)

HDRS		=	$(KOOC_HDRS:.kh=.h)

$(HDRS)		:	kooc $(KOOC_HDRS)

$(SRCS)		:	$(HDRS)
			kooc $(KOOC_SRCS)

$(NAME)		:	$(SRCS)
			gcc $(SRCS) -o $(NAME)

all		:	$(NAME)

clean		:	rm -rf $(NAME)

fclean		:	clean
			rm -rf $(HDRS)
			rm -rf $(SRCS)

re		:	fclean all

.PHONY		:	all clean fclean re
