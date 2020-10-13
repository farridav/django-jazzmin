# Bugs & Features

## Reporting bugs

When reporting bugs, or compatibility issues, here is a general guide on the best way to do it.

First of all, ask yourself these questions:

1. Does your app behave as expected if `jazzmin` is commented out of your `INSTALLED_APPS`?
2. Can you easily demonstrate the problem without code changes in our live test app https://django-jazzmin.herokuapp.com/admin/ ?
3. Can you reproduce the problem locally in our test app, and submit it as a Pull request for us to work against (see [development.md](./development.md)) ? 
4. Can you add a failing test for the problem (see [development.md](./development.md))?
5. Can you screenshot the issue and attach it to an issue or pull request?
6. Can you solve the problem (and not introduce other issues) by changing HTML, or CSS, or JS

If you can solve the problem using CSS/JS then you can temporarily use "custom CSS/JS" within jazzmin settings, see [configuration.md](./configuration.md) until we have the fix released

## Features

We welcome new features, here is a list of guidelines to consider:

1. Avoid writing too much CSS (We have CSS frameworks that we make use of, namely adminLTE & Bootstrap)
2. Look for components in AdminLTE first, we try to keep in-line with that, failing that, bootstrap has a lot to offer
3. Ensure that new features are *off* by default
4. Ensure that new features are well documented
    i) Add a section to [configuration.md](./configuration.md) if necessary
    ii) Add the new feature into the embedded test_app
5. Ensure that all configuration is optional
6. Ensure that any new strings are translated (but ideally try to use icons, or fallback on the comprehensive translations from Django)


When making changes, see if you can achieve your goal by removing code, failing that, try changing code, failing that, add new code

We prefer to use HTML first, failing that, use CSS, failing that, use JavaScript (This approach helps with maintainability) 


Some useful links for feature development:

- [https://adminlte.io/themes/v3/index3.html](https://adminlte.io/themes/v3/index3.html)
- [https://adminlte.io/docs/3.0/index.html](https://adminlte.io/docs/3.0/index.html)
- [https://fontawesome.com/icons?d=gallery&m=free](https://fontawesome.com/icons?d=gallery&m=free)
- [https://getbootstrap.com/docs/4.5/getting-started/introduction/](https://getbootstrap.com/docs/4.5/getting-started/introduction/)
