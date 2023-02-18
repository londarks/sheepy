```
database structure
                          +---------------+
                          |     User      |
                          +---------------+
                          | - id          |
                          | - name        |
                          | - address     |
                          | - email       |
                          | - phone       |
                          | - password    |
                          +---------------+
                                   ^
                                   |
                                   |
+-----------------+        +-----------------+
|     Product     |        |     Order       |
+-----------------+        +-----------------+
| - id            |        | - id            |
| - name          |        | - date          |
| - description   |        | - total_amount  |
| - price         |        | - status        |
| - quantity      |        | - user_id       |
| - image         |        +-----------------+
+-----------------+                 ^
                           +-------------------+
                           |   Order Item      |
                           +-------------------+
                           | - id              |
                           | - quantity        |
                           | - unit_price      |
                           | - discount        |
                           | - order_id        |
                           | - product_id      |
                           +-------------------+
                                    ^
                                    |
                                    |
                             +------------+
                             |   Cart     |
                             +------------+
                             | - id       |
                             | - user     |
                             +------------+
                                     ^
                                     |
                                     |
                                 +----------+
                                 |  Payment |
                                 +----------+
                                 | - id     |
                                 | - type   |
                                 | - amount |
                                 | - order  |
                                 +----------+
                                     ^
                                     |
                                     |
                           +-------------------+
                           |     Inventory     |
                           +-------------------+
                           | - id              |
                           | - product_id      |
                           | - quantity        |
                           | - last_updated    |
                           +-------------------+
```