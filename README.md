# pybalboa

[![PyPI - Version](https://img.shields.io/pypi/v/pybalboa?style=for-the-badge)](https://pypi.org/project/pybalboa/)
[![Buy Me A Coffee/Beer](https://img.shields.io/badge/Buy_Me_A_☕/🍺-F16061?style=for-the-badge&logo=ko-fi&logoColor=white&labelColor=grey)](https://ko-fi.com/natekspencer)
[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor_💜-6f42c1?style=for-the-badge&logo=github&logoColor=white&labelColor=grey)](https://github.com/sponsors/natekspencer)

[![GitHub License](https://img.shields.io/github/license/garbled1/pybalboa?style=flat-square)](LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybalboa?style=flat-square)](https://pypi.org/project/pybalboa/)
![Pepy Total Downloads](https://img.shields.io/pepy/dt/pybalboa?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pybalboa?style=flat-square)

Python Module to interface with a balboa spa

Requires Python 3 with asyncio.

To Install:

```
pip install pybalboa
```

To test:

```
python3 pybalboa <ip-of-spa-wifi> <debug-flag>
```

## To Use

See `__main__.py` for usage examples.

Minimal example:

```python
  import asyncio
  import pybalboa

  async with pybalboa.SpaClient(spa_host) as spa:
    # read/run spa commands
```

## Related

- https://github.com/ccutrer/balboa_worldwide_app/wiki - invaluable wiki for Balboa module protocol

## ❤️ Support Me

I maintain this python project in my spare time. If you find it useful, consider supporting development:

- 💜 [Sponsor me on GitHub](https://github.com/sponsors/natekspencer)
- ☕ [Buy me a coffee / beer](https://ko-fi.com/natekspencer)
- 💸 [PayPal (direct support)](https://www.paypal.com/paypalme/natekspencer)
- ⭐ [Star this project](https://github.com/garbled1/pybalboa)
- 📦 If you’d like to support in other ways, such as donating hardware for testing, feel free to [reach out to me](https://github.com/natekspencer)

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=garbled1/pybalboa)](https://www.star-history.com/#garbled1/pybalboa)
