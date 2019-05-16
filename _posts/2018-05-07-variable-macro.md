---
layout: post
title:  "可变宏macro"
date:   2018-05-07 00:00:00 +0800
categories: [cpp, note]
tags: [note]
---

~~~cpp

#define log_pet(level, dlv, format, args ...) \
    do { \
        if (log_level >= level) \
            syslog(dlv, "<%s:%d:%s> " format, __FILE__, __LINE__, __FUNCTION__, ##args); \
    } while (0)


或

#define log_pet(level, dlv, format, ...) \
    do { \
        if (log_level >= level) \
            syslog(dlv, "<%s:%d:%s> " format, __FILE__, __LINE__, __FUNCTION__,  ##__VA_ARGS__); \
    } while (0)

~~~