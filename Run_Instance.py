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
	
	getYunnan()
	getTianjin()
	getFujian()
	getInnerMongolia()
	getLiaoning()
	getChongqing()
	getGuangdong()

	# issue
	getShanghai()
	getZhejiang()
	getShandong()
	getBeijing()
	getHebei()

except:
	traceback.print_exc()

finally:
	writeText(traceback.print_exc(),'ErrorLog.txt')