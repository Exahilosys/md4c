Bindings for the `MD4C <https://github.com/mity/md4c>`_ markdown parser.

Installing
----------

.. code-block:: bash

  pip3 install md4c

Usage
-----

.. code-block:: python

  import md4c

  parser = md4c.Html()

  with open('some/doc.md') as file:
    data = file.read()

  html = parser.get(data)

  with open('some/index.html', 'w') as file:
    file.write(html)

Links
-----

- `Documentation <https://md4c.readthedocs.io>`_
