export
YOUR_UID := ${shell id -u}
YOUR_GID := ${shell id -g}

add:
	@read -p "DOIをスペース区切りで入力してください: " dois && \
	docker compose run --rm dev \
	poetry run python3 -m doi2notion add $${dois}

update:
	docker compose run --rm dev \
	poetry run python3 -m doi2notion update

dev:
	docker compose build --no-cache dev
	devcontainer open .

clean:
	docker compose down --rmi all --volumes
