import preprocessing
import scanner
import crawler
import logging
import conf
from utils import get_settings
from multiprocessing import Process
import os
import signal
import time


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def term(sig_num, addtion):
    logger.error('current pid is %s, group id is %s' % (os.getpid(), os.getpgrp()))
    os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)

def main(settings):
    """TODO: Docstring for main.
    :returns: TODO

    """
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
    settings_pre = dict(
        SCHEDULER_DUPEFILTER_KEY = 'digholes:dupefilter',
        SCHEDULER_QUEUE_KEY = 'digholes:queue_ip_pool',
        **settings
    )
    settings_scan = dict(
        SCHEDULER_QUEUE_IN_KEY = 'digholes:queue_ip_pool',
        SCHEDULER_QUEUE_OUT_KEY = 'digholes:queue_url_pool',
        **settings
    )
    settings_crawl = dict(
        SCHEDULER_QUEUE_IN_KEY = 'digholes:queue_url_pool',
        SCHEDULER_QUEUE_OUT_KEY = 'digholes:queue_response_pool',
        **settings
    )
    num_scan_host_processes = settings.get('NUM_SCAN_HOST_PROCESSES', 1)

    ps = []
    for _ in range(num_scan_host_processes):
        ps.append(Process(target=scanner.main, args=(settings_scan,), name=f'scanner_{_}'))
    ps.append(Process(target=preprocessing.main, args=(settings_pre,), name='preprocessing'))
    ps.append(Process(target=crawler.main, args=(settings_crawl,), name='crawler'))

    for p in ps:
        p.daemon = True
        p.start()
        logger.info(f'启动进程：{p.name}，进程ID：{p.pid}')
    #  解决孤儿进程问题
    signal.signal(signal.SIGTERM, term)
    #  当子进程挂了之后自动重启
    while True:
        for i, p in enumerate(ps):
            if not p.is_alive():
                logger.error('{} occured error, trying to reboot it'.format(p.name))
                ps[i] = Process(target=p._target, args=p._args, daemon=p.daemon, name=p._name)
                ps[i].start()
        time.sleep(60*5)
    for p in ps:
        p.join()

if __name__ == "__main__":
    settings = get_settings(conf)
    main(settings)


times in msec
 clock   self+sourced   self:  sourced script
 clock   elapsed:              other lines

001.000  001.000: --- VIM STARTING ---
022.000  021.000: Allocated generic buffers
024.000  002.000: locale set
024.000  000.000: clipboard setup
024.000  000.000: window checked
027.000  003.000: inits 1
066.000  039.000: parsing arguments
066.000  000.000: expanding arguments
082.000  016.000: shell init
083.000  001.000: Termcap init
083.000  000.000: inits 2
083.000  000.000: init highlight
171.000  025.000  025.000: sourcing D:\Program Files\vim\vim80\filetype.vim
172.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\ftplugin.vim
173.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\indent.vim
182.000  005.000  005.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
182.000  007.000  002.000: sourcing D:\Program Files\vim\vim80\syntax\synload.vim
183.000  009.000  002.000: sourcing D:\Program Files\vim\vim80\syntax\syntax.vim
185.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
243.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\autoload\plug.vim
326.000  002.000  002.000: sourcing D:\Program Files\vim\vim80\ftoff.vim
329.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-json\ftdetect\json.vim
331.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-coffee-script\ftdetect\coffee.vim
332.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-coffee-script\ftdetect\vim-literate-coffeescript.vim
333.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-javascript\ftdetect\javascript.vim
335.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-jst\ftdetect\jst.vim
338.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-vue\ftdetect\vue.vim
339.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-scala\ftdetect\scala.vim
341.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-less\ftdetect\less.vim
343.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-haml\ftdetect\haml.vim
345.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-markdown\ftdetect\markdown.vim
372.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\ultisnips\ftdetect\snippets.vim
373.000  022.000  022.000: sourcing D:\Program Files\vim\vim80\filetype.vim
374.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\ftplugin.vim
376.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\indent.vim
411.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\wildfire.vim\autoload\wildfire\triggers.vim
414.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
419.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
423.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
428.000  012.000  010.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-colorschemes\colors\solarized.vim
1985.000  1745.000  1706.000: sourcing D:\Program Files\vim/vimrc.bundles
1987.000  1842.000  062.000: sourcing $VIM\vimrc
1991.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax/nosyntax.vim
2003.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
2005.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
2010.000  013.000  012.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-colorschemes\colors\solarized.vim
2012.000  017.000  004.000: sourcing D:\Program Files\vim\vim80\syntax\synload.vim
2012.000  022.000  005.000: sourcing D:\Program Files\vim\vim80\syntax\syntax.vim
2016.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\filetype.vim
2018.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\ftplugin.vim
2020.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\indent.vim
2020.000  031.000  009.000: sourcing $VIMRUNTIME\defaults.vim
2020.000  064.000: sourcing vimrc file(s)
2022.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\tlib_vim\plugin\02tlib.vim
2042.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\sessionman.vim\plugin\sessionman.vim
2044.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\restore_view.vim\plugin\restore_view.vim
2047.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-over\plugin\over.vim
2051.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\incsearch.vim\plugin\incsearch.vim
2054.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\incsearch-fuzzy.vim\plugin\incsearch\fuzzy.vim
2069.000  013.000  013.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-easymotion\plugin\EasyMotion.vim
2073.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\incsearch-easymotion.vim\plugin\incsearch\easymotion.vim
2083.000  009.000  009.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-unimpaired\plugin\unimpaired.vim
2088.000  004.000  004.000: sourcing D:\Program Files\vim\vimfiles\bundle\matchit.zip\plugin\matchit.vim
2090.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\wildfire.vim\plugin\wildfire.vim
2092.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-multiple-cursors\plugin\multiple_cursors.vim
2098.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-textobj-user\autoload\textobj\user.vim
2104.000  010.000  008.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-textobj-indent\plugin\textobj\indent.vim
2106.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-textobj-sentence\plugin\textobj\sentence.vim
2109.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-textobj-quote\plugin\textobj\quote.vim
2121.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\ctrlp.vim\autoload\ctrlp\mrufiles.vim
2122.000  009.000  008.000: sourcing D:\Program Files\vim\vimfiles\bundle\ctrlp.vim\plugin\ctrlp.vim
2124.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\ctrlp-funky\plugin\funky.vim
2142.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-easygrep\autoload\EasyGrep.vim
2211.000  081.000  080.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-easygrep\plugin\EasyGrep.vim
2214.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\tagbar\plugin\tagbar.vim
2218.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\bundle\bufexplorer\plugin\bufexplorer.vim
2221.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\undotree\plugin\undotree.vim
2225.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\autoload\nerdtree.vim
2229.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\path.vim
2231.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\menu_controller.vim
2233.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\menu_item.vim
2236.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\key_map.vim
2238.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\bookmark.vim
2240.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\tree_file_node.vim
2243.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\tree_dir_node.vim
2245.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\opener.vim
2247.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\creator.vim
2250.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\flag_set.vim
2252.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\nerdtree.vim
2254.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\ui.vim
2256.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\event.vim
2257.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\notifier.vim
2260.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\autoload\nerdtree\ui_glue.vim
2286.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\nerdtree_plugin\exec_menuitem.vim
2288.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\nerdtree_plugin\fs_menu.vim
2301.000  008.000  008.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree-git-plugin\nerdtree_plugin\git_status.vim
2301.000  079.000  061.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\plugin\NERD_tree.vim
2308.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline.vim
2334.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\init.vim
2347.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\parts.vim
2348.000  044.000  043.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\plugin\airline.vim
2350.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline-themes\plugin\airline-themes.vim
2356.000  004.000  004.000: sourcing D:\Program Files\vim\vimfiles\bundle\rainbow\plugin\rainbow.vim
2358.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-signify\plugin\signify.vim
2363.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-indent-guides\autoload\indent_guides.vim
2363.000  003.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-indent-guides\plugin\indent_guides.vim
2365.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\numbers.vim\plugin\numbers.vim
2367.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\Mark--Karkat\plugin\mark.vim
2368.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-litecorrect\plugin\litecorrect.vim
2372.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-wordy\plugin\wordy.vim
2375.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-abolish\plugin\abolish.vim
2379.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-surround\plugin\surround.vim
2384.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\auto-pairs\plugin\auto-pairs.vim
2392.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\autoloclist.vim
2395.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\balloons.vim
2396.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\checker.vim
2397.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\cursor.vim
2398.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\highlighting.vim
2399.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\loclist.vim
2400.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\modemap.vim
2401.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\notifiers.vim
2402.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\registry.vim
2403.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\signs.vim
2406.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\autoload\syntastic\util.vim
2415.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\autoloclist.vim
2416.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\balloons.vim
2418.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\checker.vim
2419.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\cursor.vim
2420.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\highlighting.vim
2422.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\loclist.vim
2424.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\modemap.vim
2427.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\notifiers.vim
2429.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\registry.vim
2431.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\signs.vim
2432.000  029.000  025.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic.vim
2442.000  009.000  009.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdcommenter\plugin\NERD_commenter.vim
2445.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\tabular\plugin\Tabular.vim
2449.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\YouCompleteMe\plugin\youcompleteme.vim
2456.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\ultisnips\autoload\UltiSnips\map_keys.vim
2457.000  006.000  005.000: sourcing D:\Program Files\vim\vimfiles\bundle\ultisnips\plugin\UltiSnips.vim
2460.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-snippets\plugin\vimsnippets.vim
2462.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\gist-vim\plugin\gist.vim
2474.000  010.000  010.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-fugitive\plugin\fugitive.vim
2481.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\autoload\gitgutter\highlight.vim
2483.000  007.000  006.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\plugin\gitgutter.vim
2487.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\bundle\gitv\plugin\gitv.vim
2516.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim.vim
2531.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\util.vim
2534.000  007.000  006.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\util.vim
2537.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\common\buffers.vim
2537.000  017.000  009.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\eclim.vim
2538.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\ftdetect.vim
2539.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\ftdetect_jdt.vim
2539.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\ftdetect_sdt.vim
2552.000  012.000  012.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\java_tools.vim
2555.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\project.vim
2557.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\settings_java.vim
2558.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\settings_scala.vim
2559.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\vimplugin.vim
2561.000  072.000  038.000: sourcing D:\Program Files\vim\vimfiles\plugin\eclim.vim
2565.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\getscriptPlugin.vim
2567.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\plugin\gzip.vim
2568.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\plugin\logiPat.vim
2568.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\manpager.vim
2569.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\matchparen.vim
2571.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\plugin\netrwPlugin.vim
2572.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\plugin\rrhelper.vim
2572.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\spellfile.vim
2573.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\tarPlugin.vim
2574.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\tohtml.vim
2575.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\vimballPlugin.vim
2576.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\zipPlugin.vim
2576.000  129.000: loading plugins
2577.000  001.000: loading packages
2580.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\tabular\autoload\tabular.vim
2583.000  005.000  005.000: sourcing D:\Program Files\vim\vimfiles\bundle\tabular\after\plugin\TabularMaps.vim
2584.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\ultisnips\after\plugin\UltiSnips_after.vim
2584.000  002.000: loading after plugins
2584.000  000.000: inits 3
2586.000  002.000: reading viminfo
2586.000  000.000: setting raw mode
17557.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\autoload\gitgutter.vim
17564.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\autoload\gitgutter\utility.vim
20847.000  18259.000: waiting for return
20847.000  000.000: start termcap
20848.000  001.000: clearing screen
20851.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions.vim
20854.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\quickfix.vim
20856.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\netrw.vim
20858.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\ctrlp.vim
20861.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\undotree.vim
20864.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\hunks.vim
20867.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tagbar.vim
20871.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\branch.vim
20874.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\eclim.vim
20877.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\syntastic.vim
20880.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\whitespace.vim
20951.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\wordcount.vim
20956.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline.vim
20962.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\autoshow.vim
20966.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\tabs.vim
20969.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\buffers.vim
20972.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\ctrlspace.vim
20993.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\section.vim
20996.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\highlighter.vim
21002.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\themes.vim
21002.000  002.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline-themes\autoload\airline\themes\powerlineish.vim
21050.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\msdos.vim
21071.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\util.vim
21088.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\builder.vim
21091.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\default.vim
21116.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\autoload\syntastic\log.vim
21119.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\display\signs.vim
21121.000  258.000: opening buffers
21129.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\autoload\gitgutter\hunk.vim
21130.000  009.000: BufEnter autocommands
21130.000  000.000: editing files in windows
21136.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\YouCompleteMe\autoload\youcompleteme.vim
21757.000  626.000: VimEnter autocommands
21757.000  000.000: before starting main loop
21762.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\buflist.vim
21764.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\formatters\default.vim
21780.000  007.000  007.000: sourcing D:\Program Files\vim\vimfiles\bundle\tagbar\autoload\tagbar.vim
23623.000  1859.000: first screen update
23623.000  000.000: --- VIM STARTED ---


times in msec
 clock   self+sourced   self:  sourced script
 clock   elapsed:              other lines

000.000  000.000: --- VIM STARTING ---
019.000  019.000: Allocated generic buffers
035.000  016.000: locale set
094.000  059.000: GUI prepared
094.000  000.000: clipboard setup
094.000  000.000: window checked
096.000  002.000: inits 1
106.000  010.000: parsing arguments
106.000  000.000: expanding arguments
107.000  001.000: shell init
107.000  000.000: inits 2
107.000  000.000: init highlight
120.000  004.000  004.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
120.000  006.000  002.000: sourcing D:\Program Files\vim\vim80\syntax\synload.vim
149.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\lang\menu_zh_cn.utf-8.vim
151.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\autoload\paste.vim
228.000  082.000  081.000: sourcing D:\Program Files\vim\vim80/menu.vim
228.000  107.000  025.000: sourcing D:\Program Files\vim\vim80\filetype.vim
229.000  116.000  003.000: sourcing D:\Program Files\vim\vim80\syntax\syntax.vim
232.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\filetype.vim
234.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\ftplugin.vim
236.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\indent.vim
236.000  124.000  008.000: sourcing D:\Program Files\vim\vim80/defaults.vim
241.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\pack\dist\opt\matchit\plugin\matchit.vim
241.000  130.000  005.000: sourcing D:\Program Files\vim\vim80/vimrc_example.vim
243.000  001.000  001.000: sourcing D:\Program Files\vim\vim80/mswin.vim
244.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\filetype.vim
245.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\ftplugin.vim
247.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\indent.vim
249.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\syntax/nosyntax.vim
251.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
252.000  002.000  002.000: sourcing D:\Program Files\vim\vim80\syntax\synload.vim
252.000  004.000  001.000: sourcing D:\Program Files\vim\vim80\syntax\syntax.vim
254.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
257.000  001.000  001.000: sourcing D:\Program Files\vim\vim80/delmenu.vim
259.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\lang\menu_zh_cn.utf-8.vim
335.000  078.000  077.000: sourcing D:\Program Files\vim\vim80/menu.vim
344.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\autoload\plug.vim
393.000  002.000  002.000: sourcing D:\Program Files\vim\vim80\ftoff.vim
396.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-json\ftdetect\json.vim
398.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-coffee-script\ftdetect\coffee.vim
399.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-coffee-script\ftdetect\vim-literate-coffeescript.vim
401.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-javascript\ftdetect\javascript.vim
404.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-jst\ftdetect\jst.vim
406.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-vue\ftdetect\vue.vim
408.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-scala\ftdetect\scala.vim
410.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-less\ftdetect\less.vim
412.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-haml\ftdetect\haml.vim
414.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-markdown\ftdetect\markdown.vim
453.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\ultisnips\ftdetect\snippets.vim
454.000  031.000  031.000: sourcing D:\Program Files\vim\vim80\filetype.vim
456.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\ftplugin.vim
458.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\indent.vim
500.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\wildfire.vim\autoload\wildfire\triggers.vim
503.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
508.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
512.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
516.000  011.000  011.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-colorschemes\colors\solarized.vim
1719.000  1380.000  1333.000: sourcing D:\Program Files\vim/vimrc.bundles
1721.000  1611.000  017.000: sourcing $VIM\vimrc
1724.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\syntax/nosyntax.vim
1735.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
1738.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\syntax\syncolor.vim
1741.000  011.000  009.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-colorschemes\colors\solarized.vim
1746.000  020.000  009.000: sourcing D:\Program Files\vim\vim80\syntax\synload.vim
1746.000  022.000  002.000: sourcing D:\Program Files\vim\vim80\syntax\syntax.vim
1749.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\filetype.vim
1752.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\ftplugin.vim
1756.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\indent.vim
1756.000  033.000  011.000: sourcing $VIMRUNTIME\defaults.vim
1756.000  005.000: sourcing vimrc file(s)
1758.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\tlib_vim\plugin\02tlib.vim
1761.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\sessionman.vim\plugin\sessionman.vim
1763.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\restore_view.vim\plugin\restore_view.vim
1764.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-over\plugin\over.vim
1766.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\incsearch.vim\plugin\incsearch.vim
1769.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\incsearch-fuzzy.vim\plugin\incsearch\fuzzy.vim
1778.000  008.000  008.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-easymotion\plugin\EasyMotion.vim
1781.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\incsearch-easymotion.vim\plugin\incsearch\easymotion.vim
1793.000  010.000  010.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-unimpaired\plugin\unimpaired.vim
1795.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\matchit.zip\plugin\matchit.vim
1798.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\wildfire.vim\plugin\wildfire.vim
1800.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-multiple-cursors\plugin\multiple_cursors.vim
1805.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-textobj-user\autoload\textobj\user.vim
1811.000  009.000  008.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-textobj-indent\plugin\textobj\indent.vim
1814.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-textobj-sentence\plugin\textobj\sentence.vim
1817.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-textobj-quote\plugin\textobj\quote.vim
1821.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\ctrlp.vim\autoload\ctrlp\mrufiles.vim
1822.000  004.000  004.000: sourcing D:\Program Files\vim\vimfiles\bundle\ctrlp.vim\plugin\ctrlp.vim
1823.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\ctrlp-funky\plugin\funky.vim
1833.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-easygrep\autoload\EasyGrep.vim
1875.000  050.000  050.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-easygrep\plugin\EasyGrep.vim
1878.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\tagbar\plugin\tagbar.vim
1880.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\bufexplorer\plugin\bufexplorer.vim
1884.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\undotree\plugin\undotree.vim
1887.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\autoload\nerdtree.vim
1891.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\path.vim
1893.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\menu_controller.vim
1894.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\menu_item.vim
1896.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\key_map.vim
1899.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\bookmark.vim
1901.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\tree_file_node.vim
1904.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\tree_dir_node.vim
1905.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\opener.vim
1907.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\creator.vim
1909.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\flag_set.vim
1910.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\nerdtree.vim
1913.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\ui.vim
1915.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\event.vim
1917.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\lib\nerdtree\notifier.vim
1919.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\autoload\nerdtree\ui_glue.vim
1940.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\nerdtree_plugin\exec_menuitem.vim
1942.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\nerdtree_plugin\fs_menu.vim
1949.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree-git-plugin\nerdtree_plugin\git_status.vim
1950.000  065.000  054.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdtree\plugin\NERD_tree.vim
1953.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline.vim
1954.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\init.vim
1956.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\parts.vim
1957.000  006.000  005.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\plugin\airline.vim
1958.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline-themes\plugin\airline-themes.vim
1965.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\bundle\rainbow\plugin\rainbow.vim
1967.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-signify\plugin\signify.vim
1970.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-indent-guides\autoload\indent_guides.vim
1970.000  002.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-indent-guides\plugin\indent_guides.vim
1972.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\numbers.vim\plugin\numbers.vim
1974.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\Mark--Karkat\plugin\mark.vim
1975.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-litecorrect\plugin\litecorrect.vim
1977.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-wordy\plugin\wordy.vim
1979.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-abolish\plugin\abolish.vim
1983.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-surround\plugin\surround.vim
1985.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\auto-pairs\plugin\auto-pairs.vim
1990.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\autoloclist.vim
1991.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\balloons.vim
1992.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\checker.vim
1994.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\cursor.vim
1995.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\highlighting.vim
1996.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\loclist.vim
1998.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\modemap.vim
1999.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\notifiers.vim
2001.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\registry.vim
2002.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\signs.vim
2007.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\autoload\syntastic\util.vim
2012.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\autoloclist.vim
2014.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\balloons.vim
2015.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\checker.vim
2016.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\cursor.vim
2017.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\highlighting.vim
2019.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\loclist.vim
2020.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\modemap.vim
2021.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\notifiers.vim
2023.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\registry.vim
2024.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic\signs.vim
2027.000  024.000  020.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\plugin\syntastic.vim
2040.000  012.000  012.000: sourcing D:\Program Files\vim\vimfiles\bundle\nerdcommenter\plugin\NERD_commenter.vim
2041.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\tabular\plugin\Tabular.vim
2044.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\YouCompleteMe\plugin\youcompleteme.vim
2047.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\ultisnips\autoload\UltiSnips\map_keys.vim
2047.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\ultisnips\plugin\UltiSnips.vim
2050.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-snippets\plugin\vimsnippets.vim
2051.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\gist-vim\plugin\gist.vim
2058.000  006.000  006.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-fugitive\plugin\fugitive.vim
2063.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\autoload\gitgutter\highlight.vim
2066.000  007.000  006.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\plugin\gitgutter.vim
2070.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\bundle\gitv\plugin\gitv.vim
2093.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim.vim
2110.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\util.vim
2111.000  005.000  003.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\util.vim
2115.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\common\buffers.vim
2116.000  018.000  013.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\eclim.vim
2117.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\ftdetect.vim
2117.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\ftdetect_jdt.vim
2118.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\ftdetect_sdt.vim
2120.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\java_tools.vim
2122.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\project.vim
2124.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\settings_java.vim
2125.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\settings_scala.vim
2126.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\plugin\vimplugin.vim
2128.000  057.000  033.000: sourcing D:\Program Files\vim\vimfiles\plugin\eclim.vim
2132.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\getscriptPlugin.vim
2133.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\plugin\gzip.vim
2134.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\plugin\logiPat.vim
2134.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\manpager.vim
2135.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\matchparen.vim
2136.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\plugin\netrwPlugin.vim
2137.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\rrhelper.vim
2138.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\spellfile.vim
2139.000  001.000  001.000: sourcing D:\Program Files\vim\vim80\plugin\tarPlugin.vim
2139.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\tohtml.vim
2140.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\vimballPlugin.vim
2141.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\plugin\zipPlugin.vim
2142.000  000.000  000.000: sourcing D:\Program Files\vim\vim80\pack\dist\opt\matchit\plugin\matchit.vim
2142.000  087.000: loading plugins
2143.000  001.000: loading packages
2147.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\tabular\autoload\tabular.vim
2150.000  005.000  005.000: sourcing D:\Program Files\vim\vimfiles\bundle\tabular\after\plugin\TabularMaps.vim
2151.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\ultisnips\after\plugin\UltiSnips_after.vim
2151.000  003.000: loading after plugins
2151.000  000.000: inits 3
2153.000  001.000  001.000: sourcing $VIMRUNTIME\menu.vim
2528.000  002.000  002.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions.vim
2531.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\quickfix.vim
2535.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\netrw.vim
2538.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\ctrlp.vim
2541.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\undotree.vim
2543.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\hunks.vim
2547.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tagbar.vim
2550.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\branch.vim
2553.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\eclim.vim
2556.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\syntastic.vim
2559.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\whitespace.vim
2569.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\wordcount.vim
2573.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline.vim
2576.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\autoshow.vim
2579.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\tabs.vim
2582.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\buffers.vim
2584.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\ctrlspace.vim
2597.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\section.vim
2600.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\highlighter.vim
2607.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\themes.vim
2607.000  003.000  003.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline-themes\autoload\airline\themes\powerlineish.vim
2617.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\util.vim
2623.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\builder.vim
2626.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\default.vim
2664.000  497.000: starting GUI
2665.000  001.000: reading viminfo
2667.000  002.000: GUI delay
2667.000  000.000: setting raw mode
2667.000  000.000: start termcap
2667.000  000.000: clearing screen
2681.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\syntastic\autoload\syntastic\log.vim
2685.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\display\signs.vim
2687.000  018.000: opening buffers
2695.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\autoload\gitgutter.vim
2697.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\autoload\gitgutter\utility.vim
2701.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-gitgutter\autoload\gitgutter\hunk.vim
2701.000  012.000: BufEnter autocommands
2701.000  000.000: editing files in windows
2705.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-indent-guides\autoload\color_helper.vim
2709.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\YouCompleteMe\autoload\youcompleteme.vim
3194.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\eclim\autoload\eclim\display\menu.vim
3194.000  492.000: VimEnter autocommands
3194.000  000.000: before starting main loop
3197.000  000.000  000.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\buflist.vim
3201.000  001.000  001.000: sourcing D:\Program Files\vim\vimfiles\bundle\vim-airline\autoload\airline\extensions\tabline\formatters\default.vim
3220.000  007.000  007.000: sourcing D:\Program Files\vim\vimfiles\bundle\tagbar\autoload\tagbar.vim
5230.000  2028.000: first screen update
5230.000  000.000: --- VIM STARTED ---
