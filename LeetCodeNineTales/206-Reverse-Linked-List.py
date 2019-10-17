#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/10/17 11:53 
# @Author : Nine-Tales
# @Desc: 206-反转链表

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def reverseList(head: ListNode) -> ListNode:
    # 递归方法
    """
        if head == None or head.next == None:
        return head

    # 获取下一个节点
    next_node = head.next
    res = reverseList(next_node)
    # 将头节点接到尾部
    next_node.next = head
    head.next = None
    """

    # 非递归
    new_head = None
    while head:
        # 备份原来的head节点的next地址
        tmp = head.next
        head.next = new_head
        new_head = head
        head = tmp
    return new_head


