.PHONY: python clean

.ONESHELL:
python:

	mkdir build
	cmake -S . -B build
	make -C build
	mkdir libeep
	cp build/python/v3/pyeep.so libeep
	cp python/__init__.py libeep
	python setup.py bdist_wheel --dist-dir wheel


.ONESHELL:
clean:
	git clean -fdx
	rm -rf build
	rm -rf python/libeep
	rm -rf python/python
	rm -rf wheel