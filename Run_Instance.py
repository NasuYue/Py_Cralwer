from MajorCrawler import *

print('Instance initialize....')
# ==============================<<Main>>==============================

try:
	# easy
	getGansu()
	getHunan()
	getQinhai()
	getNingxia()
	getJiangxi()
	getJilin()
	getAnhui()
	getHainan()

	# hard
	getHenan()
	getHubei()
	getGuizhou()
	getTianjin()
	getInnerMongolia()
	#getBeijing()
	#北京另外处里
	getFujian()
	getLiaoning()
	getChongqing()
	getGuangdong()
	getShandong()

	# issue
	getHebei()
	getBeijing()
	getShanghai()
	getZhejiang()

except:
	traceback.print_exc()

finally:
	writeText(traceback.print_exc(),'ErrorLog.txt')