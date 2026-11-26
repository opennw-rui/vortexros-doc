---
nav_title: 功能特性
---


# 静态 VXLAN 功能特性

NVE 指定本端 VTEP 地址，并为每个 VNI 配置远端 VTEP 列表。发送广播、未知单播或组播时，本端向该 VNI 中的静态对端复制报文。用 `display vxlan tunnel` 查看实际隧道，用 `display vxlan statistics` 查看对应 VNI 和对端的收发量。
