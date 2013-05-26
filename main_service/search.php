<?php include('menu.php') ?>
    <div class="container">
      <div class="index_top_bg s_index_top_bg">
        <div class="index_top">
          <a href="index.php" class="logo">
            <img src="../img/logo2.png" alt="" />
          </a>
          <div class="search">
            <form class="search_box">
              <div class="right_input_bg">
              </div>
              <div class="search_input">
                <div class="search_input2">
                  <input type="text">
                  <ul class="search_input_hover" id="hover">
                    <li>
                      <a href="">Magda Gessler<span class="sih_who">autor</span></a>
                    </li>
                    <li>
                      <a href="">Magda Gessler<span class="sih_who">autor</span></a>
                    </li>
                    <li id="last">
                      <a href="">Magda Gessler<span class="sih_who">autor</span></a>
                    </li>
                  </ul>
                </div>
              </div>
              <input type="submit" value="SZUKAJ">
              <div class="search_more s_search_more">
                <a href="">
                  WYSZUKIWANIE ZAAWANSOWANE
                </a>
              </div>
            </form>
          </div>
        </div>
      </div>
      
<!--    LEFT MENU    -->
    <div class="s_left" id="s_left">
      <div class="s_arrow_zip" onclick="s_zip();"></div>
        <div class="s_left_box act" id="blue1">
          <div class="s_left_blue" onclick="s_blue('1');">
            GRUPY
            <div class="s_left_arrow">
            </div>
          </div>
          <div class="s_left_hide" >
            <div class="s_left_cat_arrow" onclick="sub('1');">
            </div>
            <div class="s_left_cat" id="btn1" onclick="btn('1');">
              Wszystkie
            </div>
            <ul id="sub1">
              <li id="li1" onclick="li('1');">
                <a>
                  Promocje  
                </a>
              </li>
              <li id="li2" onclick="li('2');">
                <a>
                  Nowości 
                </a>
              </li>
              <li id="li3" onclick="li('3');">
                <a>
                  Bestselery  
                </a>
              </li>
              <li id="li4" onclick="li('4');">
                <a>
                  Pozostale
                </a>
              </li>
            </ul>  
          </div>
          
          <div class="s_left_hide s_left_hide_last">
             <div class="s_left_cat_arrow" onclick="sub('2');">
            </div>
            <div class="s_left_cat" id="btn2" onclick="btn('2');">
              Wszystkie
            </div>
            <ul id="sub2">
              <li id="li5" onclick="li('5');">
                <a>
                  Promocje  
                </a>
              </li>
              <li id="li6" onclick="li('6');">
                <a>
                  Nowości 
                </a>
              </li>
              <li id="li7" onclick="li('7');">
                <a>
                  Bestselery  
                </a>
              </li>
              <li id="li8" onclick="li('8');">
                <a>
                  Pozostale
                </a>
              </li>
            </ul>  
             <div class="s_left_btn">
              WYCZYŚĆ
            </div>
            <div class="s_left_btn s_left_btn2">
              FILTRUJ
            </div>
          </div>
        </div>
        
        <div class="s_left_box act" id="blue2">
          <div class="s_left_blue" onclick="s_blue('2');">
            CENA
            <div class="s_left_arrow">
            </div>
          </div>
          <div class="s_left_hide">
            <form action="" method="">
              Od: <input type="text"> zł <br/>
              Do: <input type="text"> zł
            </form>
            <div class="s_left_btn">
              WYCZYŚĆ
            </div>
            <div class="s_left_btn s_left_btn2">
              FILTRUJ
            </div>
          </div>
        </div>
      </div>  
      <div class="s_right" id="s_right">
        <div class="sort">
          <div class="sort_one">
            <span style="float:left">
              CENA 
            </span>
            <div class="sort_arrow act"></div>
            <div class="sort_arrow sort_arrow_d"></div>
          </div>
          <div class="sort_one">
            <span style="float:left">
              ALFABETYCZNIE 
            </span>
            <div class="az">Az</div>
          </div>
          <div class="sort_one">
            <span style="float:left">
              PROMOCJA 
            </span>
            <div class="sort_arrow act"></div>
            <div class="sort_arrow sort_arrow_d"></div>
          </div>
          <div class="sort_one sort_one_last">
            <span style="float:left">
              ILOŚĆ FORMATÓW 
            </span>
            <div class="sort_arrow act"></div>
            <div class="sort_arrow sort_arrow_d"></div>
          </div>
          <div class="sort_ico sort_ico3"></div>
          <div class="sort_ico sort_ico2"></div>
          <div class="sort_ico sort_ico1 act"></div>
        </div>
        <div class="search_list">
          <div class="search_list_book">
            <img src="../img/bok_img_index.png" alt="" />
            <div class="s_title">
              <a href="">Krzyżacy</a>
            </div>
            <div class="s_author">
              <a href="">Henryk Sienkiewicz</a>
            </div>
            <div class="s_text">
              Formaty: Epub, PDF<br />
              Księgarnie: Woblink, Virtualo.
            </div>
             <div class="slb_price">
              cena od:
              <div class="slb_price1">
                134.99 zł
              </div>
              <a href="">
                <div class="slb_price_btn">
                  TROP <img src="../img/hand.png" alt="" />
                </div>
              </a>
              <a href="">
                <div class="slb_price_btn">
                  SZCZEGÓŁY
                </div>
              </a>
            </div>
          </div>
          <div class="search_drop" id="list_book1">
            <div class="sd_top">
              <div class="sd_top_left">
                WYŚWIETL PO:
              </div>
              <div class="sd_top_right">
                <div class="sort_for sort_for_long">WSZYSTKIE</div>
                <div class="sort_for">15</div>
                <div class="sort_for">10</div>
                <div class="sort_for">5</div>
              </div>
            </div>
            <div class="sd_format">
              <img src="../img/woblink.png" alt="" />
              <div class="sd_format_text">
                Formaty: Epub, PDF, MOBI
              </div>
              <div class="sd_price">
                32.99 <b>zł</b>
                <a href="">
                  BIERZ GO
                </a>
              </div>
            </div>
            <div class="sd_format">
              <img src="../img/woblink.png" alt="" />
              <div class="sd_format_text">
                Formaty: Epub, PDF, MOBI
              </div>
              <div class="sd_price">
                32.99 <b>zł</b>
                <a href="">
                  BIERZ GO
                </a>
              </div>
            </div>
          </div>
          <div class="search_drop_hide">
            <div class="search_drop_hide_btn" onclick="list_book('1');">
            </div>
          </div>
          
          
          <div class="search_list_book">
            <img src="../img/bok_img_index.png" alt="" />
            <div class="s_title">
              <a href="">Krzyżacy</a>
            </div>
            <div class="s_author">
              <a href="">Henryk Sienkiewicz</a>
            </div>
            <div class="s_text">
              Formaty: Epub, PDF<br />
              Księgarnie: Woblink, Virtualo.
            </div>
            <div class="slb_price">
              cena od:
              <div class="slb_price1">
                134.99 zł
              </div>
              <a href="">
                <div class="slb_price_btn">
                  TROP <img src="../img/hand.png" alt="" />
                </div>
              </a>
              <a href="">
                <div class="slb_price_btn">
                  SZCZEGÓŁY
                </div>
              </a>
            </div>
          </div>
          <div class="search_drop" id="list_book2">
            <div class="sd_top">
              <div class="sd_top_left">
                WYŚWIETL PO:
              </div>
              <div class="sd_top_right">
                <div class="sort_for sort_for_long">WSZYSTKIE</div>
                <div class="sort_for">15</div>
                <div class="sort_for">10</div>
                <div class="sort_for">5</div>
              </div>
            </div>
            <div class="sd_format">
              <img src="../img/woblink.png" alt="" />
              <div class="sd_format_text">
                Formaty: Epub, PDF, MOBI
              </div>
              <div class="sd_price">
                32.99 <b>zł</b>
                <a href="">
                  BIERZ GO
                </a>
              </div>
            </div>
            <div class="sd_format">
              <img src="../img/woblink.png" alt="" />
              <div class="sd_format_text">
                Formaty: Epub, PDF, MOBI
              </div>
              <div class="sd_price">
                32.99 <b>zł</b>
                <a href="">
                  BIERZ GO
                </a>
              </div>
            </div>
          </div>
          <div class="search_drop_hide">
            <div class="search_drop_hide_btn"  onclick="list_book('2');">
            </div>
          </div>
        </div>
        <div class="page">
          <a href="">
            <div class="page_img page_img1"></div>
          </a>
          <a href="">
            <div class="page_img page_img2"></div>
          </a>
          <div class="page_number">
            <a href="">1</a>
            <a href="">2</a>
            <a href="">3</a>
            <a href="">...</a>
            <a href="">35</a>
            <a href="">36</a>
            <a href="">37</a>
          </div>
          <a href="">
            <div class="page_img page_img3"></div>
          </a>
          <a href="">
            <div class="page_img page_img4"></div>
          </a>
          <div class="page_goto">
            <label>IDŹ DO</label> <form><input type="text"></form>
          </div>
        </div>
      </div>
     <? include("footer2.php"); ?>
  </body>
</html>