NAME = bufferapp/helpscout_api

build:
	docker build -t $(NAME) .

dev:
	docker run -it -e HELPSCOUT_API_KEY=$(HELPSCOUT_API_KEY) -v $(PWD):/usr/src/app -v $(PWD)/.ipython:/root/.ipython $(NAME) bash

test:
	docker run -e HELPSCOUT_API_KEY=$(HELPSCOUT_API_KEY) -v $(PWD):/usr/src/app -it --rm $(NAME) python -m pytest helpscout_api
