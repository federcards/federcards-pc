Feder Card PC Software
======================

This is the python3 user interface for interacting with Feder Card, a
multi-purpose credential storage smartcard. 

This software requires
[federcards-atshell](https://github.com/federcards/federcards-atshell) as
underlying proxy talking with the smartcard. For that purpose you may have to
install mono on your system.

## Feder Cards

Feder Cards are smartcards developed on [BasicCards](http://www.basiccard.com)
produced by [ZeitControl](https://www.zeitcontrol.de). Current features are

* Storage of passwords up to 100 bytes each.
* Safe storage of HOTP(or TOTP) keys. For this purpose, once a HOTP key is
  transmitted to card, it's impossible to retrieve that again, only calculated
  6-digit code can be read each time.

For maximal safety purposes, entries on card are protected with 2 passwords:

1. There is a secret key generated on card each time when an client trying talk
   to the card. The secret key is revealed to the client software only when the
   client software is told with a password that was burned into card on factory
   reset.  This password can be either entered by user, or stored in a safe
   server on the cloud(or just part of it--the user may still be required to
   type in its own share).  After the secret key is established, it is used to
   encrypt all following data transmissions between card and software.
2. The second is a PIN when accessing an encrypted storage on card. Combined
   with the shared secret in (1), this PIN is used to decrypt the entries
   on card. **This PIN is allowed to be entered ONLY ONCE, all data will lost
   once a wrong PIN is entered, thus there is no second chance.**
