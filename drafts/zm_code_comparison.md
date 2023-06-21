I've started taking a closer look at the Microsoft, `fcitx`, IBus, and RIME databases for the characters in the our proposed quote:

> 性相近也习相远也

First, for reference, here's a table of the codes obtained through the [stl56 website](http://www.stl56.com/zhengma/).

| Code | Character | Number |
| :-- | --: | --: |
| umc | 性 | 0 |
| flvv | 相 | 1 |
| pdw | 近 | 2 |
| yi | 也 | 3 |
| yt | 习 | 4 |
| flvv | 相 | 5 |
| bdrw | 远 | 6 |
| yi | 也 | 7 |

The table below, from our databases. collects all rows where *any* column contains a single character from the target string above.  It also includes any rows for *other* characters that have the *same* ZM code as one of the characters in our quote.  That is, it's looking not just for what are the codes for the characters want, but it looks at whether those same codes give us unwanted characters too.


|   | ZM Codes	| MS Characters	| fcitx Characters	| IBus Characters	| RIME Characters	| 
| --------:	| -------------	| ----------------	| ---------------	| ---------------	| -   |
| 3392	| bn	| 也 (3, 7)	| 增值	| 增值	| 增值	|  
| 3409	| bnhn	| 也 (3, 7)	|	|	|	|  
| 10830	| fl	| 协	| 相 (1, 5)	| 相 (1, 5)	| 相 (1, 5)	|  
| 11489	| fqp	| 远 (6)	|	|	|	|  
| 11494	| fqpv	| 远 (6)	|	|	|	|  
| 28938	| ntg	| 性 (0)	| 儣	| 儣	|	|  
| 28946	| ntgg	| 性 (0)	|	|	|	|  
| 29122	| nu	| 习 (4)	| 伪	| 伪	| 伪	|  
| 29137	| nud	| 买	|	|	|	|  
| 29138	| nud-	| 习 (4)	|	|	|	|  
| 37285	| rp	| 近 (2)	| 然后	| 然后	| 然后	|  
| 37341	| rpk	| 近 (2)	| 鱕	| 鱕	|	|  
| 39786	| sh	| 相 (1, 5)	| 亡	| 亡	| 亡	|  
| 39805	| shg	| 相 (1, 5)	|	|	|	|  
| 46676	| um	| 商	| 性 (0)	| 性 (0)	| 性 (0)	|  
| 46683	| umc	| 疫	| 性 (0)	| 性 (0)	| 性 (0)	|  
| 55940	| yi	| 就	| 也 (3, 7)	| 也 (3, 7)	| 也 (3, 7)	|  
| 57279	| yt	| 放	| 习 (4)	| 习 (4)	| 习 (4)	|  
| 57280	| yta	| 旗	| 习 (4)	| 习 (4)	|	|  
| 58297	| \^yi	|	| 也 (3, 7)	|	|	|  
| 58298	| \^yt	|	| 习 (4)	|	|	|  
| 58761	| \^yi-	|	| 㢭	|	|	|  
| 59135	| \^yt-	|	| 䧪	|	|	|  
| 59600	| wp	|	| 近 (2)	| 近 (2)	| 近 (2)	|  
| 59986	| brw	|	| 远 (6)	| 远 (6)	| 远 (6)	|  
| 61544	| flv	|	| 相 (1, 5)	| 相 (1, 5)	| 相 (1, 5)	|  
| 64402	| ntg-	|	| 𠆲	| 𠆲	|	|  
| 64795	| pdw	|	| 近 (2)	| 近 (2)	| 近 (2)	|  
| 67433	| wbr	|	| 冠	| 冠	| 远 (6)	|  
| 67434	| wbr-	|	| 远 (6)	| 远 (6)	|	|  
| 67640	| wpd	|	| 近 (2)	| 近 (2)	| 近 (2)	|  
| 71191	| bdrw	|	| 远 (6)	| 远 (6)	| 远 (6)	|  
| 71192	| bdrw-	|	| 𪓣	| 𪓣	|	|  
| 86721	| flvv	|	| 相 (1, 5)	| 相 (1, 5)	| 相 (1, 5)	|  
| 134229	| wbrd	|	| 远 (6)	| 远 (6)	| 远 (6)	|  
| 193680	| yi-	|	|	|	| 那些   |

The table can be a little confusing to sift through, and I'm still trying to make sure I see all the details, but for now here are some points to note.

* Where you see a `'-'` in a ZM code, that's something I had to insert.  There are codes where a single ZM code represents two or more different Chinese characters.  To make sure I didn't overwrite a previous correspondence while gathering the data, I added `'-'` to any ZM code that was already in the database and had a Chinese character assigned.
	* In short, treat ZM codes with `'-'` as if they didn't have it: e.g. `'yi-'` and `'yi'` are the *same code*.
* I've numbered the characters in our quote from 0 to 7, so that we could keep track of them in the data table.
	* If you focus on a specific column, you can look for 0, 1, 2, ..., 7 in order and verify that each database represented here does in fact contain all the characters.
* You can also see that **no database (column) _uniquely_ assigns one code to one character**.
	* In each database, each character appears at least twice (... except for 也 (3, 7) in the RIME database).  That means at least two codes can represent the same character: e.g. `'pdw'` and `'wpd'` both represent 近 (2).
	* And you see many `'-'`s, which means that frequently the same code can represent *two* characters (or character strings): e.g. 
		* `'wbr'` can represent 远 (6) or 冠 in the `fcitx` and IBus databases;
		* `'yi'` can represent 也 (3, 7) or 那些 in the RIME database;
		* `'nud'` can represent 习 (4) or 买 in the Microsoft database.
* **Practical Upshot: we need a _heuristic_ to resolve the ambiguities**, regardless of the database we choose.
	* This gets us back to the situation with the 4-corner codes: there we resolved the ambiguities through considering frequency.  Here we might try something else.
	* We could **try using the longest code available for each character**, assuming that shorter codes are "shortcuts".
		* We will still run into trouble with the code `'bdrw`', representing 远 (6), but also another character which, for some reason I haven't understood yet, doesn't render in the `fcitx` and IBus databases.
			* But we can see on the [stl56 website](http://www.stl56.com/zhengma/) that even there `'bdrw'` corresponds to two characters, if I'm understanding the output properly: 远 (6) and 黿.
			* We could try using the code `'wbrd'` (I'm not sure what our heuristic would be for choosing that code over the other, since they're the same length).  But the website doesn't render any characters for that code, if I'm understanding correctly.
	* We could **try using the shortest code available for each character**.
		* This seems to work for the Microsoft database, though it doesn't give the codes y'all got from the website.
		* This doesn't seem to work for the character 远 (6) in the `fcitx`, IBus, and RIME databases, since that could have code `'brw'` or `'wbr'`.


