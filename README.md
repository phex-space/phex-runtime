# phex-runtime
Runtime Library for the phex.space

To manage th dependencies of the project, you need to install [poetry](https://python-poetry.org/).

You should start by setting up your runtime with ```poetry install``` and ```poetry shell```. Within the resulting shell you can run the tests with the following command:

```bash
pytest --cov=phex.runtime --cov-report=term --cov-report=html ./tests
```
