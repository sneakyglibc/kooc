NAME		=	project_using_kooc

KOOC_SRCS	=	test.kc			\

SRCS		=	$(KOOC_SRCS:.kc=.c)

$(SRCS)		:	kooc $(KOOC_SRCS)

koockies	:	
			./kooc $(KOOC_SRCS)

$(NAME)		:	koockies
			gcc $(SRCS) -o $(NAME)

clean		:	rm -rf $(NAME)

fclean		:	clean
			rm -rf $(SRCS)

re		:	fclean all

.PHONY		:	all koockies clean fclean re
