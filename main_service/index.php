<?php include('menu.php') ?>
    <div class="container">
      <div class="index_top_bg">
        <div class="index_top">
          <a href="index.php" class="logo">
            <img src="../img/logo.png" alt="" />
          </a>
          <div class="social">
            ODWIEDŹ NAS: 
            <a href="">
              <img src="../img/social_f.png" alt="" /> 
            </a> 
            <a href="">
              <img src="../img/social_t.png" alt="" /> 
            </a> 
            <a href="">
              <img src="../img/social_g.png" alt="" /> 
            </a>  
          </div>
          <div class="search">
            <div class="search_text">
              Pomożemy Ci znaleść najlepszą ofertę<br />
              na <b>ebooka</b> lub <b>audiobooka</b>:
            </div>
            <form action="search.php" class="search_box">
              <div class="search_input">
                <div class="search_input2">
                  <input type="text">
                  <ul class="search_input_hover">
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
              <div class="search_more">
                <a href="">
                  Wyszukiwanie zaawansowane
                </a>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="index_bottom">
        <div class="index_title">U nas porownasz <b>2222222 ofert z 22 księgarni!</b></div>
        <div class="index_subtitle">
          <img src="../img/red_line.png" alt="" />BESTSELLERY<img src="../img/red_line.png" alt="" />
        </div>
        <div class="index_subtitle">
          <img src="../img/red_line.png" alt="" />NOWOŚCI<img src="../img/red_line.png" alt="" />
        </div>
        <div class="index_subtitle">
          <img src="../img/red_line.png" alt="" />PROMOCJE<img src="../img/red_line.png" alt="" />
        </div>
        
  <!--   list book       -->
      <? for($j=0;$j<3;$j++){ ?>
        <div class="three_index_box">
          <? for($i=0;$i<3;$i++){ ?>
          <div class="index_box">
            <img src="../img/bok_img_index.png" alt="" />
            <div class="ib_text">
              <div class="ib_text1">
                <a href="">
                  Więzień nieba. Książe Parnasu
                </a>
              </div>
              <div class="ib_text2">
                <a href="">
                  Zafon Carlos Louis
                </a>
              </div>
              <div class="ib_text_pos">
                <div class="ib_text3">
                  cena od:
                </div>
                <div class="ib_price">
                  29.99<span class="ib_price2">zł</span>
                </div>
                <div class="ib_line">
                </div>
                <a href="">
                  <div class="ib_btn">  
                  </div>
                </a>
                <a href="">
                  <div class="ib_btn2">
                    SPRAWDŹ
                  </div>
                </a>
              </div>  
            </div>
            <div class="index_box_h">
              <div class="ibh_image">
                <a href="">
                  Dostępne<br /> 
                  formaty:
                  <div class="ibh_image_format">
                    epub<br />
                    pdf<br />
                    mp3
                  </div>
                </a>  
              </div>
              <div class="x">
              </div>
            </div>
          </div>
          <? } ?>
          <div class="index_more">
            <a href="">
              Zobacz więcej
            </a>
          </div>
        </div>
      <? } ?>
        
   <!--  end of list book       -->  
 
     </div>
     
     <?php include("footer.php"); ?>
     
  </body>
</html>