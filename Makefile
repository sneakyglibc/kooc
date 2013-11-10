NAME		=	project_using_kooc

KOOC_SRCS	=	test.kc			\

SRCS		=	$(KOOC_SRCS:.kc=.c)

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
