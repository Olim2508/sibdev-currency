migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

suser:
	docker-compose exec web python manage.py createsuperuser

logs:
	docker-compose logs -f web

down:
	docker-compose down

build_up:
	docker-compose up -d --build

down_db:
	docker-compose down -v

up:
	docker-compose up -d

test:
	docker-compose exec web python manage.py test