# Linked quest display

Previous there was a `Submit Item`, `Item information` button at the end, but since multiple items may be required
it will be changed.

Example message structure:

```
[ Text Display                                                              ]
[ ### Task: Submit 154.26 / 219 kg grape to Sakuya.                         ]
[                                                                           ]
[ We are running low on wine in the mansion.                                ]
[                                                                           ]
I would like to request a great amount of grapes.                           ]
[                                                                           ]
[**Rewards:**                                                               ]
[- **40000** (emoji)                                                        ]
[- **50** credibility                                                       ]
[**Duration:**                                                              ]
[- **9 days**                                                               ]
[**Time left:**                                                             ]
[- **7 days, 8 hours, 44 minutes**                                          ]
[**Completed:**                                                             ]
[- **0 / unlimited** times, cannot be re-accepted                           ]

[ Separator                                                                 ]

[ Row                                                                       ]
[ [ Button         ] [ Button  ] [ Button      ][ Button    ]               ]
[ [ View my quests ] [ Abandon ] [ Auto submit ][ <dynamic> ]               ]
```

The order of a buttons and their features change a little. As an example there will be a new `Auto submit` button,
which would just auto submit whatever you have on you.

The dynamic button can be any of the following depending on the amount of requirements:

Multiple:
```
[ Button                           ]
[ Select requirement to submit for ]
```

Single:
```
[ Button                ]
[ Select item to submit ]
```

### Requirement select

If a quest has multiple requirements a message like the following would be displayed:

```
[ Text display                                                              ]
[ ### Select a requirement to submit for                                    ]

[ Separator                                                                 ]

...

[ Separator                                                                 ]

[ Row                                                                       ]
[ [ Button        ] [ Button        ] [ Button          ] [ Button       ]  ]
[ [ (emoji Page 0 ] [ (emoji Page 2 ] [ (emoji) Refresh ] [ (emoji) Back ]  ]
```

Depending on the requirements, the inside would be different.

Single item required:
```
[ Text display                                                      ]
[ 87.48 / 219 kg (emoji) **Bluefrankish**, 123 on stock (12.23 kg)  ]

[ Row                                                               ]
[ [ Button                ] [ Button           ]                    ]
[ [ Submit items          ] [ Item information ]                    ]
```

Multiple item requirement:
```
[ Text display                                                      ]
[ 2 / 14 **Skull**, 24 in stock                                     ]

[ Row                                                               ]
[ [ Button                 ]                                        ]
[ [ Select items to submit ]                                        ]
```

It would always display how much you have from them.
If you have no items, the `Submit` button of any kind would be disabled.
If you already completed the requirement, the button would be grayed out and disabled.


How much is required and how much you have in the stock and it in units would be displayed.

### Item select

If a requirement allows selecting multiple items, a message of the following structure would be displayed:

```
[ Text display                                                              ]
[ ### Select items to submit                                                ]
[                                                                           ]
[ 2 / 14 **Skull**                                                          ]

[ Separator                                                                 ]

[ Text display                                                              ]
[ (emoji) **Fairy skull**, 11 in stock                                      ]

[ Row                                                                       ]
[ [ Button            ] [ Button           ]                                ]
[ [ Submit items      ] [ Item information ]                                ]

[ Separator                                                                 ]

[ Text display                                                              ]
[ (emoji) **Human skull**, 13 in stock                                      ]

[ Row                                                                       ]
[ [ Button            ] [ Button           ]                                ]
[ [ Submit items      ] [ Item information ]                                ]

[ Separator                                                                 ]

[ Row                                                                       ]
[ [ Button         ] [ Button         ] [ Button          ] [ Button       ]]
[ [ (emoji) Page 0 ] [ (emoji) Page 2 ] [ (emoji) Refresh ] [ (emoji) Back ]]
```

How much is required would be displayed at the top, while how much you have from each, next to the options.
