# CHANGELOG - process

## 1.7.0 / 2019-01-04

* [Added] Support Python 3. See [#2812][1].

## 1.6.0 / 2018-11-30

* [Added] Update psutil. See [#2576][2].

## 1.5.0 / 2018-10-12

* [Added] Upgrade psutil. See [#2190][3].

## 1.4.0 / 2018-09-04

* [Added] Added regex support to process check when exact_match is False.. See [#2055][4]. Thanks [asandeep][5].
* [Added] [Add] Add cpu.normalized_pct metric. See [#1729][6].
* [Fixed] Add data files to the wheel package. See [#1727][7].

## 1.3.0 / 2018-02-13

* [FEATURE] Add option to use sudo for privileged process checks on file descriptors. See [#1530][8], thanks [@pdecat][9].

## 1.2.0 / 2018-01-10

* [IMPROVEMENT] Filter processes by user. See [#337][10]

## 1.1.2 / 2017-08-28

* [IMPROVEMENT] Better logging when a process was not found. See [#609][11]

## 1.1.1 / 2017-07-18

* [BUGFIX] Make process validation case-insensitve on Windows See [#479][12]

## 1.1.0 / 2017-06-05

* [FEATURE] Add option to collect metrics for children of matched processes. See [#425][13]

## 1.0.1 / 2017-05-11

* [BUGFIX] Handle the case where the pidfile doesn't exist. See [#349][14]

## 1.0.0 / 2017-05-08

* [FEATURE] adds process integration.

<!--- The following link definition list is generated by PimpMyChangelog --->
[1]: https://github.com/DataDog/integrations-core/pull/2812
[2]: https://github.com/DataDog/integrations-core/pull/2576
[3]: https://github.com/DataDog/integrations-core/pull/2190
[4]: https://github.com/DataDog/integrations-core/pull/2055
[5]: https://github.com/asandeep
[6]: https://github.com/DataDog/integrations-core/pull/1729
[7]: https://github.com/DataDog/integrations-core/pull/1727
[8]: 
[9]: https://github.com/pdecat
[10]: https://github.com/DataDog/integrations-core/pull/337
[11]: https://github.com/DataDog/integrations-core/pull/609
[12]: https://github.com/DataDog/integrations-core/pull/479
[13]: https://github.com/DataDog/integrations-core/issues/425
[14]: https://github.com/DataDog/integrations-core/issues/349
