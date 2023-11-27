.PHONY: all test clean

all: 	venv
	@echo "Building virtual environment..."
	@source venv/bin/activate; \
	echo "Installing dependencies..."; \
	python ./setup.py install
	@echo "Build completed successfully."

venv:
	@echo "Creating virtual environment..."
	@python -m venv venv; \
	source venv/bin/activate; \
	echo "Installing requirements..."; \
	pip install -r ./requirements.txt

test: 	all
	@echo "Running tests..."
	@source venv/bin/activate; \
	python -m unittest discover
	@echo "Running performance tests..."
	@source venv/bin/activate; \
	python ./cjson_performance_test.py


clean:
	@echo "Cleaning up..."
	@rm -rf venv build dist cjson.egg-info
	@echo "Cleanup completed."