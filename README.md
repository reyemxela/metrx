# metrx

A simple and extensible metrics collection system for InfluxDB.

## About
This project came about because I was wanting to monitor services that don't already have support from tools like [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) or [Varken](https://github.com/Boerderij/Varken).

I also wanted to make something easily extensible, even at runtime. Along with the included modules (which will grow and improve over time), metrx will also dynamically load modules on startup. See [Extending](#extending) for more info.

## Configuration
Copy `config.example.yaml` to `config.yaml` and edit as needed. Each service needs at least the `type`, `interval`, and `config` keys. The keys under `config` will depend on the type of service module being used.

## Usage

### Docker/Podman CLI:
```bash
docker run \
  --name metrx \
  -v /path/to/config/folder:/config \
  -v /path/to/custom/modules:/app/modules/custom \ #optional
  ghcr.io/reyemxela/metrx:latest

# alternate config mount: -v ./config.yaml:/config/config.yaml
```

## Extending

When bind-mounting `/app/modules/custom`, metrx will dynamically load any `*.py` files found, allowing totally custom modules to be used. See `__template.py` in the modules directory for the basic layout needed.

Modules found in `custom` also override any built-in modules with the same name.

_**Docker/Podman:**_ Additionally, if a `requirements.txt` file is present in the `custom` folder, `pip` will attempt to install from it on container startup, so custom modules can use any 3rd-party libraries needed.

## Contributing

Starting out, I'm mainly focusing on including support for services I'm personally running and monitoring, but PRs are more than welcome!