TESTCASE = [
    {
        "test_name": "test_tpch_sql_2",
        "file_names": ["part_1.parquet", "supplier_1.parquet",
                       "partsupp_1.parquet", "nation_1.parquet",
                       "region_1.parquet", "partsupp_1.parquet",
                       "supplier_1.parquet", "nation_1.parquet",
                       "region_1.parquet"],
        "sql_query":
            """
            SELECT
                s_acctbal,
                s_name,
                n_name,
                p_partkey,
                p_mfgr,
                s_address,
                s_phone,
                s_comment
            FROM
                '{}', '{}', '{}', '{}', '{}'
            WHERE
                p_partkey = ps_partkey
                AND s_suppkey = ps_suppkey
                AND p_size = 15
                AND p_type LIKE '%BRASS'
                AND s_nationkey = n_nationkey
                AND n_regionkey = r_regionkey
                AND r_name = 'EUROPE'
                AND ps_supplycost = (
                    SELECT
                        min(ps_supplycost)
                    FROM
                        '{}', '{}', '{}', '{}'
                    WHERE
                        p_partkey = ps_partkey
                        AND s_suppkey = ps_suppkey
                        AND s_nationkey = n_nationkey
                        AND n_regionkey = r_regionkey
                        AND r_name = 'EUROPE')
            ORDER BY
                s_acctbal DESC,
                n_name,
                s_name,
                p_partkey
            LIMIT 100;
            """,
        "substrait_query":
            """
            {
              "extensionUris": [{
                "extensionUriAnchor": 1,
                "uri": "/functions_boolean.yaml"
              }, {
                "extensionUriAnchor": 3,
                "uri": "/functions_string.yaml"
              }, {
                "extensionUriAnchor": 4,
                "uri": "/functions_arithmetic_decimal.yaml"
              }, {
                "extensionUriAnchor": 2,
                "uri": "/functions_comparison.yaml"
              }],
              "extensions": [{
                "extensionFunction": {
                  "extensionUriReference": 1,
                  "functionAnchor": 0,
                  "name": "and:bool"
                }
              }, {
                "extensionFunction": {
                  "extensionUriReference": 2,
                  "functionAnchor": 1,
                  "name": "equal:any1_any1"
                }
              }, {
                "extensionFunction": {
                  "extensionUriReference": 3,
                  "functionAnchor": 2,
                  "name": "like:vchar_vchar"
                }
              }, {
                "extensionFunction": {
                  "extensionUriReference": 4,
                  "functionAnchor": 3,
                  "name": "min:decimal"
                }
              }],
              "relations": [{
                "root": {
                  "input": {
                    "fetch": {
                      "common": {
                        "direct": {
                        }
                      },
                      "input": {
                        "sort": {
                          "common": {
                            "direct": {
                            }
                          },
                          "input": {
                            "project": {
                              "common": {
                                "emit": {
                                  "outputMapping": [28, 29, 30, 31, 32, 33, 34, 35]
                                }
                              },
                              "input": {
                                "filter": {
                                  "common": {
                                    "direct": {
                                    }
                                  },
                                  "input": {
                                    "join": {
                                      "common": {
                                        "direct": {
                                        }
                                      },
                                      "left": {
                                        "join": {
                                          "common": {
                                            "direct": {
                                            }
                                          },
                                          "left": {
                                            "join": {
                                              "common": {
                                                "direct": {
                                                }
                                              },
                                              "left": {
                                                "join": {
                                                  "common": {
                                                    "direct": {
                                                    }
                                                  },
                                                  "left": {
                                                    "read": {
                                                      "common": {
                                                        "direct": {
                                                        }
                                                      },
                                                      "baseSchema": {
                                                        "names": ["P_PARTKEY", "P_NAME", "P_MFGR", "P_BRAND", "P_TYPE", "P_SIZE", "P_CONTAINER", "P_RETAILPRICE", "P_COMMENT"],
                                                        "struct": {
                                                          "types": [{
                                                            "i64": {
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_REQUIRED"
                                                            }
                                                          }, {
                                                            "varchar": {
                                                              "length": 55,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "fixedChar": {
                                                              "length": 25,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "fixedChar": {
                                                              "length": 10,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "varchar": {
                                                              "length": 25,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "i32": {
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "fixedChar": {
                                                              "length": 10,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "decimal": {
                                                              "scale": 0,
                                                              "precision": 19,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "varchar": {
                                                              "length": 23,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }],
                                                          "typeVariationReference": 0,
                                                          "nullability": "NULLABILITY_REQUIRED"
                                                        }
                                                      },
                                                     "local_files": {
                                                         "items": [
                                                         {
                                                             "uri_file": "file://FILENAME_PLACEHOLDER_0",
                                                             "format": "FILE_FORMAT_PARQUET"
                                                         }
                                                         ]
                                                     }
                                                    }
                                                  },
                                                  "right": {
                                                    "read": {
                                                      "common": {
                                                        "direct": {
                                                        }
                                                      },
                                                      "baseSchema": {
                                                        "names": ["S_SUPPKEY", "S_NAME", "S_ADDRESS", "S_NATIONKEY", "S_PHONE", "S_ACCTBAL", "S_COMMENT"],
                                                        "struct": {
                                                          "types": [{
                                                            "i64": {
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_REQUIRED"
                                                            }
                                                          }, {
                                                            "fixedChar": {
                                                              "length": 25,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "varchar": {
                                                              "length": 40,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "i64": {
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_REQUIRED"
                                                            }
                                                          }, {
                                                            "fixedChar": {
                                                              "length": 15,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "decimal": {
                                                              "scale": 0,
                                                              "precision": 19,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }, {
                                                            "varchar": {
                                                              "length": 101,
                                                              "typeVariationReference": 0,
                                                              "nullability": "NULLABILITY_NULLABLE"
                                                            }
                                                          }],
                                                          "typeVariationReference": 0,
                                                          "nullability": "NULLABILITY_REQUIRED"
                                                        }
                                                      },
                                                     "local_files": {
                                                         "items": [
                                                         {
                                                             "uri_file": "file://FILENAME_PLACEHOLDER_1",
                                                             "format": "FILE_FORMAT_PARQUET"
                                                         }
                                                         ]
                                                     }
                                                    }
                                                  },
                                                  "expression": {
                                                    "literal": {
                                                      "boolean": true,
                                                      "nullable": false,
                                                      "typeVariationReference": 0
                                                    }
                                                  },
                                                  "type": "JOIN_TYPE_INNER"
                                                }
                                              },
                                              "right": {
                                                "read": {
                                                  "common": {
                                                    "direct": {
                                                    }
                                                  },
                                                  "baseSchema": {
                                                    "names": ["PS_PARTKEY", "PS_SUPPKEY", "PS_AVAILQTY", "PS_SUPPLYCOST", "PS_COMMENT"],
                                                    "struct": {
                                                      "types": [{
                                                        "i64": {
                                                          "typeVariationReference": 0,
                                                          "nullability": "NULLABILITY_REQUIRED"
                                                        }
                                                      }, {
                                                        "i64": {
                                                          "typeVariationReference": 0,
                                                          "nullability": "NULLABILITY_REQUIRED"
                                                        }
                                                      }, {
                                                        "i32": {
                                                          "typeVariationReference": 0,
                                                          "nullability": "NULLABILITY_NULLABLE"
                                                        }
                                                      }, {
                                                        "decimal": {
                                                          "scale": 0,
                                                          "precision": 19,
                                                          "typeVariationReference": 0,
                                                          "nullability": "NULLABILITY_NULLABLE"
                                                        }
                                                      }, {
                                                        "varchar": {
                                                          "length": 199,
                                                          "typeVariationReference": 0,
                                                          "nullability": "NULLABILITY_NULLABLE"
                                                        }
                                                      }],
                                                      "typeVariationReference": 0,
                                                      "nullability": "NULLABILITY_REQUIRED"
                                                    }
                                                  },
                                                     "local_files": {
                                                         "items": [
                                                         {
                                                             "uri_file": "file://FILENAME_PLACEHOLDER_2",
                                                             "format": "FILE_FORMAT_PARQUET"
                                                         }
                                                         ]
                                                     }
                                                }
                                              },
                                              "expression": {
                                                "literal": {
                                                  "boolean": true,
                                                  "nullable": false,
                                                  "typeVariationReference": 0
                                                }
                                              },
                                              "type": "JOIN_TYPE_INNER"
                                            }
                                          },
                                          "right": {
                                            "read": {
                                              "common": {
                                                "direct": {
                                                }
                                              },
                                              "baseSchema": {
                                                "names": ["N_NATIONKEY", "N_NAME", "N_REGIONKEY", "N_COMMENT"],
                                                "struct": {
                                                  "types": [{
                                                    "i64": {
                                                      "typeVariationReference": 0,
                                                      "nullability": "NULLABILITY_REQUIRED"
                                                    }
                                                  }, {
                                                    "fixedChar": {
                                                      "length": 25,
                                                      "typeVariationReference": 0,
                                                      "nullability": "NULLABILITY_NULLABLE"
                                                    }
                                                  }, {
                                                    "i64": {
                                                      "typeVariationReference": 0,
                                                      "nullability": "NULLABILITY_REQUIRED"
                                                    }
                                                  }, {
                                                    "varchar": {
                                                      "length": 152,
                                                      "typeVariationReference": 0,
                                                      "nullability": "NULLABILITY_NULLABLE"
                                                    }
                                                  }],
                                                  "typeVariationReference": 0,
                                                  "nullability": "NULLABILITY_REQUIRED"
                                                }
                                              },
                                                 "local_files": {
                                                     "items": [
                                                     {
                                                         "uri_file": "file://FILENAME_PLACEHOLDER_3",
                                                         "format": "FILE_FORMAT_PARQUET"
                                                     }
                                                     ]
                                                 }
                                            }
                                          },
                                          "expression": {
                                            "literal": {
                                              "boolean": true,
                                              "nullable": false,
                                              "typeVariationReference": 0
                                            }
                                          },
                                          "type": "JOIN_TYPE_INNER"
                                        }
                                      },
                                      "right": {
                                        "read": {
                                          "common": {
                                            "direct": {
                                            }
                                          },
                                          "baseSchema": {
                                            "names": ["R_REGIONKEY", "R_NAME", "R_COMMENT"],
                                            "struct": {
                                              "types": [{
                                                "i64": {
                                                  "typeVariationReference": 0,
                                                  "nullability": "NULLABILITY_REQUIRED"
                                                }
                                              }, {
                                                "fixedChar": {
                                                  "length": 25,
                                                  "typeVariationReference": 0,
                                                  "nullability": "NULLABILITY_NULLABLE"
                                                }
                                              }, {
                                                "varchar": {
                                                  "length": 152,
                                                  "typeVariationReference": 0,
                                                  "nullability": "NULLABILITY_NULLABLE"
                                                }
                                              }],
                                              "typeVariationReference": 0,
                                              "nullability": "NULLABILITY_REQUIRED"
                                            }
                                          },
                                             "local_files": {
                                                 "items": [
                                                 {
                                                     "uri_file": "file://FILENAME_PLACEHOLDER_4",
                                                     "format": "FILE_FORMAT_PARQUET"
                                                 }
                                                 ]
                                             }
                                        }
                                      },
                                      "expression": {
                                        "literal": {
                                          "boolean": true,
                                          "nullable": false,
                                          "typeVariationReference": 0
                                        }
                                      },
                                      "type": "JOIN_TYPE_INNER"
                                    }
                                  },
                                  "condition": {
                                    "scalarFunction": {
                                      "functionReference": 0,
                                      "args": [],
                                      "outputType": {
                                        "bool": {
                                          "typeVariationReference": 0,
                                          "nullability": "NULLABILITY_NULLABLE"
                                        }
                                      },
                                      "arguments": [{
                                        "value": {
                                          "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [],
                                            "outputType": {
                                              "bool": {
                                                "typeVariationReference": 0,
                                                "nullability": "NULLABILITY_REQUIRED"
                                              }
                                            },
                                            "arguments": [{
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 0
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }, {
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 16
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }]
                                          }
                                        }
                                      }, {
                                        "value": {
                                          "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [],
                                            "outputType": {
                                              "bool": {
                                                "typeVariationReference": 0,
                                                "nullability": "NULLABILITY_REQUIRED"
                                              }
                                            },
                                            "arguments": [{
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 9
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }, {
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 17
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }]
                                          }
                                        }
                                      }, {
                                        "value": {
                                          "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [],
                                            "outputType": {
                                              "bool": {
                                                "typeVariationReference": 0,
                                                "nullability": "NULLABILITY_NULLABLE"
                                              }
                                            },
                                            "arguments": [{
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 5
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }, {
                                              "value": {
                                                "literal": {
                                                  "i32": 15,
                                                  "nullable": false,
                                                  "typeVariationReference": 0
                                                }
                                              }
                                            }]
                                          }
                                        }
                                      }, {
                                        "value": {
                                          "scalarFunction": {
                                            "functionReference": 2,
                                            "args": [],
                                            "outputType": {
                                              "bool": {
                                                "typeVariationReference": 0,
                                                "nullability": "NULLABILITY_NULLABLE"
                                              }
                                            },
                                            "arguments": [{
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 4
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }, {
                                              "value": {
                                                "cast": {
                                                  "type": {
                                                    "varchar": {
                                                      "length": 25,
                                                      "typeVariationReference": 0,
                                                      "nullability": "NULLABILITY_NULLABLE"
                                                    }
                                                  },
                                                  "input": {
                                                    "literal": {
                                                      "fixedChar": "%BRASS",
                                                      "nullable": false,
                                                      "typeVariationReference": 0
                                                    }
                                                  },
                                                  "failureBehavior": "FAILURE_BEHAVIOR_UNSPECIFIED"
                                                }
                                              }
                                            }]
                                          }
                                        }
                                      }, {
                                        "value": {
                                          "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [],
                                            "outputType": {
                                              "bool": {
                                                "typeVariationReference": 0,
                                                "nullability": "NULLABILITY_REQUIRED"
                                              }
                                            },
                                            "arguments": [{
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 12
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }, {
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 21
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }]
                                          }
                                        }
                                      }, {
                                        "value": {
                                          "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [],
                                            "outputType": {
                                              "bool": {
                                                "typeVariationReference": 0,
                                                "nullability": "NULLABILITY_REQUIRED"
                                              }
                                            },
                                            "arguments": [{
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 23
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }, {
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 25
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }]
                                          }
                                        }
                                      }, {
                                        "value": {
                                          "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [],
                                            "outputType": {
                                              "bool": {
                                                "typeVariationReference": 0,
                                                "nullability": "NULLABILITY_NULLABLE"
                                              }
                                            },
                                            "arguments": [{
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 26
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }, {
                                              "value": {
                                                "cast": {
                                                  "type": {
                                                    "fixedChar": {
                                                      "length": 25,
                                                      "typeVariationReference": 0,
                                                      "nullability": "NULLABILITY_REQUIRED"
                                                    }
                                                  },
                                                  "input": {
                                                    "literal": {
                                                      "fixedChar": "EUROPE",
                                                      "nullable": false,
                                                      "typeVariationReference": 0
                                                    }
                                                  },
                                                  "failureBehavior": "FAILURE_BEHAVIOR_UNSPECIFIED"
                                                }
                                              }
                                            }]
                                          }
                                        }
                                      }, {
                                        "value": {
                                          "scalarFunction": {
                                            "functionReference": 1,
                                            "args": [],
                                            "outputType": {
                                              "bool": {
                                                "typeVariationReference": 0,
                                                "nullability": "NULLABILITY_NULLABLE"
                                              }
                                            },
                                            "arguments": [{
                                              "value": {
                                                "selection": {
                                                  "directReference": {
                                                    "structField": {
                                                      "field": 19
                                                    }
                                                  },
                                                  "rootReference": {
                                                  }
                                                }
                                              }
                                            }, {
                                              "value": {
                                                "subquery": {
                                                  "scalar": {
                                                    "input": {
                                                      "aggregate": {
                                                        "common": {
                                                          "direct": {
                                                          }
                                                        },
                                                        "input": {
                                                          "project": {
                                                            "common": {
                                                              "emit": {
                                                                "outputMapping": [19]
                                                              }
                                                            },
                                                            "input": {
                                                              "filter": {
                                                                "common": {
                                                                  "direct": {
                                                                  }
                                                                },
                                                                "input": {
                                                                  "join": {
                                                                    "common": {
                                                                      "direct": {
                                                                      }
                                                                    },
                                                                    "left": {
                                                                      "join": {
                                                                        "common": {
                                                                          "direct": {
                                                                          }
                                                                        },
                                                                        "left": {
                                                                          "join": {
                                                                            "common": {
                                                                              "direct": {
                                                                              }
                                                                            },
                                                                            "left": {
                                                                              "read": {
                                                                                "common": {
                                                                                  "direct": {
                                                                                  }
                                                                                },
                                                                                "baseSchema": {
                                                                                  "names": ["PS_PARTKEY", "PS_SUPPKEY", "PS_AVAILQTY", "PS_SUPPLYCOST", "PS_COMMENT"],
                                                                                  "struct": {
                                                                                    "types": [{
                                                                                      "i64": {
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_REQUIRED"
                                                                                      }
                                                                                    }, {
                                                                                      "i64": {
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_REQUIRED"
                                                                                      }
                                                                                    }, {
                                                                                      "i32": {
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                                      }
                                                                                    }, {
                                                                                      "decimal": {
                                                                                        "scale": 0,
                                                                                        "precision": 19,
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                                      }
                                                                                    }, {
                                                                                      "varchar": {
                                                                                        "length": 199,
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                                      }
                                                                                    }],
                                                                                    "typeVariationReference": 0,
                                                                                    "nullability": "NULLABILITY_REQUIRED"
                                                                                  }
                                                                                },
                                                                                 "local_files": {
                                                                                     "items": [
                                                                                     {
                                                                                         "uri_file": "file://FILENAME_PLACEHOLDER_5",
                                                                                         "format": "FILE_FORMAT_PARQUET"
                                                                                     }
                                                                                     ]
                                                                                 }
                                                                              }
                                                                            },
                                                                            "right": {
                                                                              "read": {
                                                                                "common": {
                                                                                  "direct": {
                                                                                  }
                                                                                },
                                                                                "baseSchema": {
                                                                                  "names": ["S_SUPPKEY", "S_NAME", "S_ADDRESS", "S_NATIONKEY", "S_PHONE", "S_ACCTBAL", "S_COMMENT"],
                                                                                  "struct": {
                                                                                    "types": [{
                                                                                      "i64": {
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_REQUIRED"
                                                                                      }
                                                                                    }, {
                                                                                      "fixedChar": {
                                                                                        "length": 25,
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                                      }
                                                                                    }, {
                                                                                      "varchar": {
                                                                                        "length": 40,
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                                      }
                                                                                    }, {
                                                                                      "i64": {
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_REQUIRED"
                                                                                      }
                                                                                    }, {
                                                                                      "fixedChar": {
                                                                                        "length": 15,
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                                      }
                                                                                    }, {
                                                                                      "decimal": {
                                                                                        "scale": 0,
                                                                                        "precision": 19,
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                                      }
                                                                                    }, {
                                                                                      "varchar": {
                                                                                        "length": 101,
                                                                                        "typeVariationReference": 0,
                                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                                      }
                                                                                    }],
                                                                                    "typeVariationReference": 0,
                                                                                    "nullability": "NULLABILITY_REQUIRED"
                                                                                  }
                                                                                },
                                                                                 "local_files": {
                                                                                     "items": [
                                                                                     {
                                                                                         "uri_file": "file://FILENAME_PLACEHOLDER_6",
                                                                                         "format": "FILE_FORMAT_PARQUET"
                                                                                     }
                                                                                     ]
                                                                                 }
                                                                              }
                                                                            },
                                                                            "expression": {
                                                                              "literal": {
                                                                                "boolean": true,
                                                                                "nullable": false,
                                                                                "typeVariationReference": 0
                                                                              }
                                                                            },
                                                                            "type": "JOIN_TYPE_INNER"
                                                                          }
                                                                        },
                                                                        "right": {
                                                                          "read": {
                                                                            "common": {
                                                                              "direct": {
                                                                              }
                                                                            },
                                                                            "baseSchema": {
                                                                              "names": ["N_NATIONKEY", "N_NAME", "N_REGIONKEY", "N_COMMENT"],
                                                                              "struct": {
                                                                                "types": [{
                                                                                  "i64": {
                                                                                    "typeVariationReference": 0,
                                                                                    "nullability": "NULLABILITY_REQUIRED"
                                                                                  }
                                                                                }, {
                                                                                  "fixedChar": {
                                                                                    "length": 25,
                                                                                    "typeVariationReference": 0,
                                                                                    "nullability": "NULLABILITY_NULLABLE"
                                                                                  }
                                                                                }, {
                                                                                  "i64": {
                                                                                    "typeVariationReference": 0,
                                                                                    "nullability": "NULLABILITY_REQUIRED"
                                                                                  }
                                                                                }, {
                                                                                  "varchar": {
                                                                                    "length": 152,
                                                                                    "typeVariationReference": 0,
                                                                                    "nullability": "NULLABILITY_NULLABLE"
                                                                                  }
                                                                                }],
                                                                                "typeVariationReference": 0,
                                                                                "nullability": "NULLABILITY_REQUIRED"
                                                                              }
                                                                            },
                                                                             "local_files": {
                                                                                 "items": [
                                                                                 {
                                                                                     "uri_file": "file://FILENAME_PLACEHOLDER_7",
                                                                                     "format": "FILE_FORMAT_PARQUET"
                                                                                 }
                                                                                 ]
                                                                             }
                                                                          }
                                                                        },
                                                                        "expression": {
                                                                          "literal": {
                                                                            "boolean": true,
                                                                            "nullable": false,
                                                                            "typeVariationReference": 0
                                                                          }
                                                                        },
                                                                        "type": "JOIN_TYPE_INNER"
                                                                      }
                                                                    },
                                                                    "right": {
                                                                      "read": {
                                                                        "common": {
                                                                          "direct": {
                                                                          }
                                                                        },
                                                                        "baseSchema": {
                                                                          "names": ["R_REGIONKEY", "R_NAME", "R_COMMENT"],
                                                                          "struct": {
                                                                            "types": [{
                                                                              "i64": {
                                                                                "typeVariationReference": 0,
                                                                                "nullability": "NULLABILITY_REQUIRED"
                                                                              }
                                                                            }, {
                                                                              "fixedChar": {
                                                                                "length": 25,
                                                                                "typeVariationReference": 0,
                                                                                "nullability": "NULLABILITY_NULLABLE"
                                                                              }
                                                                            }, {
                                                                              "varchar": {
                                                                                "length": 152,
                                                                                "typeVariationReference": 0,
                                                                                "nullability": "NULLABILITY_NULLABLE"
                                                                              }
                                                                            }],
                                                                            "typeVariationReference": 0,
                                                                            "nullability": "NULLABILITY_REQUIRED"
                                                                          }
                                                                        },
                                                                        "local_files": {
                                                                             "items": [
                                                                             {
                                                                                 "uri_file": "file://FILENAME_PLACEHOLDER_8",
                                                                                 "format": "FILE_FORMAT_PARQUET"
                                                                             }
                                                                             ]
                                                                         }
                                                                      }
                                                                    },
                                                                    "expression": {
                                                                      "literal": {
                                                                        "boolean": true,
                                                                        "nullable": false,
                                                                        "typeVariationReference": 0
                                                                      }
                                                                    },
                                                                    "type": "JOIN_TYPE_INNER"
                                                                  }
                                                                },
                                                                "condition": {
                                                                  "scalarFunction": {
                                                                    "functionReference": 0,
                                                                    "args": [],
                                                                    "outputType": {
                                                                      "bool": {
                                                                        "typeVariationReference": 0,
                                                                        "nullability": "NULLABILITY_NULLABLE"
                                                                      }
                                                                    },
                                                                    "arguments": [{
                                                                      "value": {
                                                                        "scalarFunction": {
                                                                          "functionReference": 1,
                                                                          "args": [],
                                                                          "outputType": {
                                                                            "bool": {
                                                                              "typeVariationReference": 0,
                                                                              "nullability": "NULLABILITY_REQUIRED"
                                                                            }
                                                                          },
                                                                          "arguments": [{
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 0
                                                                                  }
                                                                                },
                                                                                "outerReference": {
                                                                                  "stepsOut": 1
                                                                                }
                                                                              }
                                                                            }
                                                                          }, {
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 0
                                                                                  }
                                                                                },
                                                                                "rootReference": {
                                                                                }
                                                                              }
                                                                            }
                                                                          }]
                                                                        }
                                                                      }
                                                                    }, {
                                                                      "value": {
                                                                        "scalarFunction": {
                                                                          "functionReference": 1,
                                                                          "args": [],
                                                                          "outputType": {
                                                                            "bool": {
                                                                              "typeVariationReference": 0,
                                                                              "nullability": "NULLABILITY_REQUIRED"
                                                                            }
                                                                          },
                                                                          "arguments": [{
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 5
                                                                                  }
                                                                                },
                                                                                "rootReference": {
                                                                                }
                                                                              }
                                                                            }
                                                                          }, {
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 1
                                                                                  }
                                                                                },
                                                                                "rootReference": {
                                                                                }
                                                                              }
                                                                            }
                                                                          }]
                                                                        }
                                                                      }
                                                                    }, {
                                                                      "value": {
                                                                        "scalarFunction": {
                                                                          "functionReference": 1,
                                                                          "args": [],
                                                                          "outputType": {
                                                                            "bool": {
                                                                              "typeVariationReference": 0,
                                                                              "nullability": "NULLABILITY_REQUIRED"
                                                                            }
                                                                          },
                                                                          "arguments": [{
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 8
                                                                                  }
                                                                                },
                                                                                "rootReference": {
                                                                                }
                                                                              }
                                                                            }
                                                                          }, {
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 12
                                                                                  }
                                                                                },
                                                                                "rootReference": {
                                                                                }
                                                                              }
                                                                            }
                                                                          }]
                                                                        }
                                                                      }
                                                                    }, {
                                                                      "value": {
                                                                        "scalarFunction": {
                                                                          "functionReference": 1,
                                                                          "args": [],
                                                                          "outputType": {
                                                                            "bool": {
                                                                              "typeVariationReference": 0,
                                                                              "nullability": "NULLABILITY_REQUIRED"
                                                                            }
                                                                          },
                                                                          "arguments": [{
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 14
                                                                                  }
                                                                                },
                                                                                "rootReference": {
                                                                                }
                                                                              }
                                                                            }
                                                                          }, {
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 16
                                                                                  }
                                                                                },
                                                                                "rootReference": {
                                                                                }
                                                                              }
                                                                            }
                                                                          }]
                                                                        }
                                                                      }
                                                                    }, {
                                                                      "value": {
                                                                        "scalarFunction": {
                                                                          "functionReference": 1,
                                                                          "args": [],
                                                                          "outputType": {
                                                                            "bool": {
                                                                              "typeVariationReference": 0,
                                                                              "nullability": "NULLABILITY_NULLABLE"
                                                                            }
                                                                          },
                                                                          "arguments": [{
                                                                            "value": {
                                                                              "selection": {
                                                                                "directReference": {
                                                                                  "structField": {
                                                                                    "field": 17
                                                                                  }
                                                                                },
                                                                                "rootReference": {
                                                                                }
                                                                              }
                                                                            }
                                                                          }, {
                                                                            "value": {
                                                                              "cast": {
                                                                                "type": {
                                                                                  "fixedChar": {
                                                                                    "length": 25,
                                                                                    "typeVariationReference": 0,
                                                                                    "nullability": "NULLABILITY_REQUIRED"
                                                                                  }
                                                                                },
                                                                                "input": {
                                                                                  "literal": {
                                                                                    "fixedChar": "EUROPE",
                                                                                    "nullable": false,
                                                                                    "typeVariationReference": 0
                                                                                  }
                                                                                },
                                                                                "failureBehavior": "FAILURE_BEHAVIOR_UNSPECIFIED"
                                                                              }
                                                                            }
                                                                          }]
                                                                        }
                                                                      }
                                                                    }]
                                                                  }
                                                                }
                                                              }
                                                            },
                                                            "expressions": [{
                                                              "selection": {
                                                                "directReference": {
                                                                  "structField": {
                                                                    "field": 3
                                                                  }
                                                                },
                                                                "rootReference": {
                                                                }
                                                              }
                                                            }]
                                                          }
                                                        },
                                                        "groupings": [{
                                                          "groupingExpressions": []
                                                        }],
                                                        "measures": [{
                                                          "measure": {
                                                            "functionReference": 3,
                                                            "args": [],
                                                            "sorts": [],
                                                            "phase": "AGGREGATION_PHASE_INITIAL_TO_RESULT",
                                                            "outputType": {
                                                              "decimal": {
                                                                "scale": 0,
                                                                "precision": 19,
                                                                "typeVariationReference": 0,
                                                                "nullability": "NULLABILITY_NULLABLE"
                                                              }
                                                            },
                                                            "invocation": "AGGREGATION_INVOCATION_ALL",
                                                            "arguments": [{
                                                              "value": {
                                                                "selection": {
                                                                  "directReference": {
                                                                    "structField": {
                                                                      "field": 0
                                                                    }
                                                                  },
                                                                  "rootReference": {
                                                                  }
                                                                }
                                                              }
                                                            }]
                                                          }
                                                        }]
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }]
                                          }
                                        }
                                      }]
                                    }
                                  }
                                }
                              },
                              "expressions": [{
                                "selection": {
                                  "directReference": {
                                    "structField": {
                                      "field": 14
                                    }
                                  },
                                  "rootReference": {
                                  }
                                }
                              }, {
                                "selection": {
                                  "directReference": {
                                    "structField": {
                                      "field": 10
                                    }
                                  },
                                  "rootReference": {
                                  }
                                }
                              }, {
                                "selection": {
                                  "directReference": {
                                    "structField": {
                                      "field": 22
                                    }
                                  },
                                  "rootReference": {
                                  }
                                }
                              }, {
                                "selection": {
                                  "directReference": {
                                    "structField": {
                                      "field": 0
                                    }
                                  },
                                  "rootReference": {
                                  }
                                }
                              }, {
                                "selection": {
                                  "directReference": {
                                    "structField": {
                                      "field": 2
                                    }
                                  },
                                  "rootReference": {
                                  }
                                }
                              }, {
                                "selection": {
                                  "directReference": {
                                    "structField": {
                                      "field": 11
                                    }
                                  },
                                  "rootReference": {
                                  }
                                }
                              }, {
                                "selection": {
                                  "directReference": {
                                    "structField": {
                                      "field": 13
                                    }
                                  },
                                  "rootReference": {
                                  }
                                }
                              }, {
                                "selection": {
                                  "directReference": {
                                    "structField": {
                                      "field": 15
                                    }
                                  },
                                  "rootReference": {
                                  }
                                }
                              }]
                            }
                          },
                          "sorts": [{
                            "expr": {
                              "selection": {
                                "directReference": {
                                  "structField": {
                                    "field": 0
                                  }
                                },
                                "rootReference": {
                                }
                              }
                            },
                            "direction": "SORT_DIRECTION_DESC_NULLS_FIRST"
                          }, {
                            "expr": {
                              "selection": {
                                "directReference": {
                                  "structField": {
                                    "field": 2
                                  }
                                },
                                "rootReference": {
                                }
                              }
                            },
                            "direction": "SORT_DIRECTION_ASC_NULLS_LAST"
                          }, {
                            "expr": {
                              "selection": {
                                "directReference": {
                                  "structField": {
                                    "field": 1
                                  }
                                },
                                "rootReference": {
                                }
                              }
                            },
                            "direction": "SORT_DIRECTION_ASC_NULLS_LAST"
                          }, {
                            "expr": {
                              "selection": {
                                "directReference": {
                                  "structField": {
                                    "field": 3
                                  }
                                },
                                "rootReference": {
                                }
                              }
                            },
                            "direction": "SORT_DIRECTION_ASC_NULLS_LAST"
                          }]
                        }
                      },
                      "offset": "0",
                      "count": "100"
                    }
                  },
                  "names": ["S_ACCTBAL", "S_NAME", "N_NAME", "P_PARTKEY", "P_MFGR", "S_ADDRESS", "S_PHONE", "S_COMMENT"]
                }
              }],
              "expectedTypeUrls": []
            }
            """,
    }
]