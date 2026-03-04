%----------------------------------------------------------------------------------------
%   studyGuide.cls - Grade 7 Math (Fun & Colorful Edition)
%   Adapted from the college-level Study Guide class for young learners.
%----------------------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{studyGuide}[2025/02/07 Grade 7 Math - Fun & Colorful Edition]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax
\LoadClass{book}
\raggedbottom   % prevent vertical glue stretching between elements

%----------------------------------------------------------------------------------------
%   REQUIRED PACKAGES
%----------------------------------------------------------------------------------------
\usepackage{graphicx}
\graphicspath{{icons/}{images/}{../../VM_common_sections/Images/}}

\usepackage{float}
\usepackage[usenames, dvipsnames, svgnames, table]{xcolor}
\usepackage{calc}
\usepackage{changepage}
\usepackage{etoolbox}
\usepackage{setspace}
\setstretch{1.4} % Slightly more spacing for young readers
\usepackage{environ}
\usepackage{multicol}
\usepackage{needspace}
\usepackage[most]{tcolorbox}

%----------------------------------------------------------------------------------------
%   COLORS - Grade 7 Fun Color Palette
%----------------------------------------------------------------------------------------
\RequirePackage{VM_packages/VMfunColors}

%----------------------------------------------------------------------------------------
%   GEOMETRY / MARGINS
%----------------------------------------------------------------------------------------
\usepackage{geometry}
\geometry{
    paperwidth=8.5in,
    paperheight=11in,
    top=2cm,
    bottom=2.8cm,
    inner=2cm,
    outer=1.5cm,
    headsep=10pt,
    headheight=15pt,
    footskip=2.2cm,
    columnsep=1cm,
}

%----------------------------------------------------------------------------------------
%   FONTS - Fun, rounded, kid-friendly for Grade 7  (XeLaTeX + fontspec)
%----------------------------------------------------------------------------------------
% We use Comic Neue (OTF via fontspec) as the main body font — polished,
% friendly, rounded.  All fonts are loaded as OpenType/TrueType so edges
% stay perfectly smooth at every zoom level.
%
% ALTERNATIVES — change \setmainfont / \setsansfont below:
%   Option A — Nunito (geometric, very rounded, modern):
%       \setmainfont{Nunito}[Path=…/nunito/, Extension=.otf,
%         UprightFont=*-Regular, BoldFont=*-Bold,
%         ItalicFont=*-Italic, BoldItalicFont=*-BoldItalic]
%   Option B — Cabin (humanist, slightly rounded, clean):
%       \setmainfont{Cabin}[Path=…/cabin/, Extension=.otf, …]
%   Option C — Arial Rounded MT Bold (system, single weight):
%       \setmainfont{ArialRoundedMTBold}
%
% COVER FONT OPTIONS (used by VMfunCover.sty for the state name):
%   Helvetica Neue Bold  — HelveticaNeue-Bold   (clean, slightly rounded)
%   Arial Rounded MT Bold — ArialRoundedMTBold   (rounded corners, kid-friendly)
%   Nunito Black          — Nunito-Black.otf     (very rounded geometric)
%   Nunito ExtraBold      — Nunito-ExtraBold.otf (rounded geometric, lighter)
%   Chalkboard SE Bold    — ChalkboardSE-Bold    (playful chalk style)
%----------------------------------------------------------------------------------------
\usepackage{fontspec}
\defaultfontfeatures{Ligatures=TeX}

\setmainfont{ComicNeue}[
    Path           = /usr/local/texlive/2025/texmf-dist/fonts/opentype/rozynski/comicneue/,
    Extension      = .otf,
    UprightFont    = ComicNeue-Regular,
    BoldFont       = ComicNeue-Bold,
    ItalicFont     = ComicNeue-RegularItalic,
    BoldItalicFont = ComicNeue-BoldItalic,
]
\setsansfont{ComicNeue}[
    Path           = /usr/local/texlive/2025/texmf-dist/fonts/opentype/rozynski/comicneue/,
    Extension      = .otf,
    UprightFont    = ComicNeue-Regular,
    BoldFont       = ComicNeue-Bold,
    ItalicFont     = ComicNeue-RegularItalic,
    BoldItalicFont = ComicNeue-BoldItalic,
]

\usepackage{microtype}             % Improve typography (limited features under XeTeX)
\usepackage{fontawesome5}          % 1600+ professional icons
\usepackage{qrcode}                 % QR code generation for footer

%----------------------------------------------------------------------------------------
%   HEADERS AND FOOTERS
%----------------------------------------------------------------------------------------
\usepackage{fancyhdr}
\pagestyle{fancy}

\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\chaptermark}[1]{\markboth{\sffamily\normalsize\bfseries\chaptername\ \thechapter.~#1}{}}
\renewcommand{\sectionmark}[1]{\markright{\sffamily\normalsize\thesection~#1}{}}

\fancyhf{}
\fancyhead[LE,RO]{\sffamily\thepage}
\fancyhead[LO]{\rightmark}
\fancyhead[RE]{\leftmark}

% --- Footer parameters (override with \renewcommand in main .tex) ---
\providecommand{\VMFooterURL}{https://viewmath.com/grade7}
\providecommand{\VMFooterURLDisplay}{ViewMath.com/Grade7}
\providecommand{\VMFooterGetOnlineImg}{get_online.pdf}
\providecommand{\VMFooterHandImg}{hand-point-cartoon-left.png}
\providecommand{\VMFooterLogoImg}{ViewMath.com.pdf}

% --- Footer design: VMfooter-style (Get Online + QR + hand + ViewMath logo) ---
\newcommand{\vmFooterLeft}{%
    \raisebox{0.5cm}{%
    \begin{minipage}[b]{0.55\textwidth}
        \begin{tabular}{@{}l@{}l@{}l@{}}
            \raisebox{-0.45cm}{\includegraphics[height=1.1cm]{\VMFooterGetOnlineImg}} \hspace*{0.1cm}&
            \raisebox{0cm}{\qrcode*[height=1.1cm]{\VMFooterURL}} & \hspace{5pt}
            \begin{tabular}{@{}l@{}}
                \raisebox{-0.1cm}[0pt][0pt]{\footnotesize\sffamily Find more at} \\
                \raisebox{0cm}[0pt][0pt]{\href{\VMFooterURL}{\footnotesize\sffamily\bfseries \VMFooterURLDisplay}} \\[0cm]
                \raisebox{0cm}{\includegraphics[height=0.5cm]{\VMFooterHandImg}}
            \end{tabular}
        \end{tabular}
    \end{minipage}%
    }%
}
\newcommand{\vmFooterRight}{%
    \raisebox{0.4cm}{\includegraphics[height=0.9cm]{\VMFooterLogoImg}}%
}

\fancyfoot[L]{\vmFooterLeft}
\fancyfoot[R]{\vmFooterRight}

\fancypagestyle{plain}{
    \fancyhead{}
    \renewcommand{\headrulewidth}{0pt}
    \fancyfoot[L]{\vmFooterLeft}
    \fancyfoot[R]{\vmFooterRight}
}

\usepackage{emptypage}

%----------------------------------------------------------------------------------------
%   SECTION STYLING - Fun and colorful for Grade 7
%----------------------------------------------------------------------------------------
\setcounter{secnumdepth}{3}

\usepackage[
    explicit,
    newparttoc,
]{titlesec}

%-------------------------------------------
% CHAPTER STYLING - Full-page chapter opener
%-------------------------------------------
\newcommand{\thechapterimage}{}
\newcommand{\chapterimage}[1]{\renewcommand{\thechapterimage}{#1}}

\newcommand{\thechapterspaceabove}{}
\newcommand{\chapterspaceabove}[1]{\renewcommand{\thechapterspaceabove}{#1}}

\newcommand{\thechapterspacebelow}{}
\newcommand{\chapterspacebelow}[1]{\renewcommand{\thechapterspacebelow}{#1}}

%-------------------------------------------
% Full-page chapter opener design
%   #1 = chapter number (empty for unnumbered)
%   #2 = chapter title text
%-------------------------------------------
\newcommand{\fullChapterPage}[2]{%
    \thispagestyle{empty}%
    \startcontents[chapters]%
    %
    \begin{tikzpicture}[remember picture, overlay]
        %
        % ============ BACKGROUND ============
        % Light tinted full page
        \fill[funBlue!4]
            (current page.south west) rectangle (current page.north east);
        %
        % ============ TOP BLUE BAND ============
        % Main band covering top ~40% of page
        \fill[funBlue!90]
            (current page.north west) rectangle
            ([yshift=-11cm]current page.north east);
        %
        % Slight diagonal accent at bottom of band
        \fill[funBlue!70]
            ([yshift=-11cm]current page.north west) --
            ([yshift=-11cm]current page.north east) --
            ([yshift=-12cm]current page.north east) --
            ([yshift=-11.5cm]current page.north west) -- cycle;
        %
        % ============ DECORATIVE CIRCLES ============
        \fill[white, opacity=0.06]
            ([xshift=-3cm, yshift=-2cm]current page.north east) circle (5cm);
        \fill[white, opacity=0.04]
            ([xshift=2.5cm, yshift=-7cm]current page.north west) circle (3.5cm);
        \fill[white, opacity=0.03]
            ([xshift=8cm, yshift=-1cm]current page.north west) circle (2cm);
        %
        % ============ DECORATIVE STARS ============
        \node[opacity=0.20] at ([xshift=2.2cm, yshift=-1.5cm]current page.north west)
            {\textcolor{funYellow}{\fontsize{28}{30}\selectfont\faStar}};
        \node[opacity=0.14] at ([xshift=-2.2cm, yshift=-1.8cm]current page.north east)
            {\textcolor{funYellow}{\fontsize{20}{22}\selectfont\faStar}};
        \node[opacity=0.10] at ([xshift=-3.5cm, yshift=-9cm]current page.north east)
            {\textcolor{white}{\fontsize{18}{20}\selectfont\faStar}};
        \node[opacity=0.08] at ([xshift=5cm, yshift=-9.5cm]current page.north west)
            {\textcolor{funYellow}{\fontsize{14}{16}\selectfont\faStar}};
        %
        % ============ CHAPTER NUMBER & TITLE ============
        \expandafter\ifstrequal\expandafter{#1}{}{%
            % ---- Unnumbered chapter ----
            \node[
                text width=0.75\paperwidth, align=center,
                font=\fontsize{30}{36}\selectfont\sffamily\bfseries\color{white},
            ] at ([yshift=-6cm]current page.north) {#2};
        }{%
            % ---- Numbered chapter ----
            % "CHAPTER" label
            \node[
                font=\fontsize{13}{16}\selectfont\sffamily\color{white!65!funBlue},
                inner sep=0pt,
            ] at ([yshift=-2.6cm]current page.north)
                {C\kern0.12em H\kern0.12em A\kern0.12em P\kern0.12em T\kern0.12em E\kern0.12em R};
            %
            % Shadow behind number circle
            \fill[funBlueDark, opacity=0.25]
                ([xshift=1mm, yshift=-5.1cm]current page.north) circle (1.4cm);
            %
            % Chapter number in yellow circle
            \node[
                circle, fill=funYellow, draw=funYellowDark, line width=2pt,
                inner sep=0pt, minimum size=2.8cm,
                font=\fontsize{34}{38}\selectfont\sffamily\bfseries\color{funBlueDark},
            ] at ([yshift=-5cm]current page.north) {#1};
            %
            % Chapter title
            \node[
                text width=0.78\paperwidth, align=center,
                font=\fontsize{26}{32}\selectfont\sffamily\bfseries\color{white},
            ] at ([yshift=-8cm]current page.north) {#2};
        }%
        %
        % ============ DECORATIVE DIVIDER ============
        \draw[funYellow, line width=2pt]
            ([xshift=4cm, yshift=-10cm]current page.north west) --
            ([xshift=-4cm, yshift=-10cm]current page.north east);
        \node at ([yshift=-10cm]current page.north)
            {\textcolor{funYellow}{\large\faStar}};
        %
        % ============ MINI TABLE OF CONTENTS ============
        % Only show for numbered chapters (unnumbered ones like Answer Key have no sections)
        \expandafter\ifstrequal\expandafter{#1}{}{}{%
        \node[anchor=north, inner sep=0pt] at ([yshift=-13.5cm]current page.north) {%
            \begin{minipage}{\textwidth}%
            \begin{tcolorbox}[
                enhanced,
                colback=white,
                colframe=funBlue!30,
                colbacktitle=funBlue!70,
                coltitle=white,
                fonttitle=\Large\bfseries\sffamily,
                title={\iconStar[0.5cm]\hspace{3mm}What's Inside\hspace{3mm}\iconStar[0.5cm]},
                halign title=center,
                arc=10pt,
                outer arc=10pt,
                boxrule=1.5pt,
                width=\textwidth,
                top=2mm, bottom=2mm,
                left=4mm, right=4mm,
                toptitle=3mm, bottomtitle=3mm,
                shadow={2mm}{-2mm}{0mm}{funBlue!8},
            ]
                {\footnotesize\printcontents[chapters]{l}{1}{\setcounter{tocdepth}{1}}}
            \end{tcolorbox}%
            \end{minipage}%
        };%
        }
        %
        % ============ BOTTOM DECORATIONS ============
        % Owl mascot at bottom right
        \node[opacity=0.5] at ([xshift=-3cm, yshift=3cm]current page.south east)
            {\iconOwl[2cm]};
        %
        % Stars at bottom
        \node[opacity=0.12] at ([xshift=3cm, yshift=2.5cm]current page.south west)
            {\textcolor{funBlue}{\fontsize{24}{26}\selectfont\faStar}};
        \node[opacity=0.08] at ([xshift=7cm, yshift=1.5cm]current page.south west)
            {\textcolor{funYellow}{\fontsize{18}{20}\selectfont\faStar}};
        %
        % Small accent dots
        \foreach \x/\y in {4.5/-2.5, 8/-1.2, 13.5/-3.5, 16/-1.8} {
            \fill[white, opacity=0.12]
                ([xshift=\x cm, yshift=\y cm]current page.north west) circle (2pt);
        }
        %
    \end{tikzpicture}%
    %
    \newpage
}

% Numbered chapters
\titleformat
{\chapter}
[block]
{}
{}
{0cm}
{\fullChapterPage{\thechapter}{#1}}
[]

% Unnumbered chapters
\titleformat
{name=\chapter, numberless}
[block]
{}
{}
{0cm}
{\fullChapterPage{}{#1}}
[]

\titlespacing*{\chapter}{0pt}{0pt}{0pt}

%-------------------------------------------
% PRACTICE TEST START PAGE
%   Full-page design used in practice test books
%   instead of the chapter opener.
%   #1 = test number (displayed prominently)
%   #2 = number of questions (e.g. 30)
%-------------------------------------------
\newcommand{\practiceTestPage}[2]{%
    \cleardoublepage
    \thispagestyle{empty}%
    % Step chapter counter for answer key grouping, reset problems
    \refstepcounter{chapter}%
    \setcounter{funProblem}{0}%
    \addcontentsline{toc}{chapter}{Practice Test #1}%
    \markboth{\sffamily\normalsize\bfseries Practice Test #1}%
             {\sffamily\normalsize\bfseries Practice Test #1}%
    %
    \begin{tikzpicture}[remember picture, overlay]
        %
        % ============ BACKGROUND ============
        \fill[funTeal!4]
            (current page.south west) rectangle (current page.north east);
        %
        % ============ TOP TEAL BAND ============
        \fill[funTeal!85]
            (current page.north west) rectangle
            ([yshift=-11cm]current page.north east);
        %
        % Diagonal accent
        \fill[funTeal!65]
            ([yshift=-11cm]current page.north west) --
            ([yshift=-11cm]current page.north east) --
            ([yshift=-12cm]current page.north east) --
            ([yshift=-11.5cm]current page.north west) -- cycle;
        %
        % ============ DECORATIVE CIRCLES ============
        \fill[white, opacity=0.06]
            ([xshift=-3cm, yshift=-2cm]current page.north east) circle (5cm);
        \fill[white, opacity=0.04]
            ([xshift=2.5cm, yshift=-7cm]current page.north west) circle (3.5cm);
        \fill[white, opacity=0.03]
            ([xshift=8cm, yshift=-1cm]current page.north west) circle (2cm);
        %
        % ============ DECORATIVE STARS ============
        \node[opacity=0.20] at ([xshift=2.2cm, yshift=-1.5cm]current page.north west)
            {\textcolor{funYellow}{\fontsize{28}{30}\selectfont\faStar}};
        \node[opacity=0.14] at ([xshift=-2.2cm, yshift=-1.8cm]current page.north east)
            {\textcolor{funYellow}{\fontsize{20}{22}\selectfont\faStar}};
        \node[opacity=0.10] at ([xshift=-3.5cm, yshift=-9cm]current page.north east)
            {\textcolor{white}{\fontsize{18}{20}\selectfont\faStar}};
        \node[opacity=0.08] at ([xshift=5cm, yshift=-9.5cm]current page.north west)
            {\textcolor{funYellow}{\fontsize{14}{16}\selectfont\faStar}};
        %
        % ============ "PRACTICE TEST" LABEL ============
        \node[
            font=\fontsize{13}{16}\selectfont\sffamily\color{white!65!funTeal},
            inner sep=0pt,
        ] at ([yshift=-2.6cm]current page.north)
            {P\kern0.12em R\kern0.12em A\kern0.12em C\kern0.12em T\kern0.12em I\kern0.12em C\kern0.12em E%
             \hspace{0.5em}T\kern0.12em E\kern0.12em S\kern0.12em T};
        %
        % ============ TEST NUMBER IN YELLOW CIRCLE ============
        \fill[funTealDark, opacity=0.25]
            ([xshift=1mm, yshift=-5.1cm]current page.north) circle (1.4cm);
        \node[
            circle, fill=funYellow, draw=funYellowDark, line width=2pt,
            inner sep=0pt, minimum size=2.8cm,
            font=\fontsize{34}{38}\selectfont\sffamily\bfseries\color{funTealDark},
        ] at ([yshift=-5cm]current page.north) {#1};
        %
        % ============ TITLE ============
        \node[
            text width=0.78\paperwidth, align=center,
            font=\fontsize{26}{32}\selectfont\sffamily\bfseries\color{white},
        ] at ([yshift=-8cm]current page.north) {Practice Test #1};
        %
        % ============ QUESTION COUNT ============
        \node[
            font=\fontsize{14}{18}\selectfont\sffamily\color{white!80!funTeal},
        ] at ([yshift=-9.5cm]current page.north)
            {\faClipboardCheck\hspace{2mm}#2 Questions};
        %
        % ============ DECORATIVE DIVIDER ============
        \draw[funYellow, line width=2pt]
            ([xshift=4cm, yshift=-10.5cm]current page.north west) --
            ([xshift=-4cm, yshift=-10.5cm]current page.north east);
        \node at ([yshift=-10.5cm]current page.north)
            {\textcolor{funYellow}{\large\faStar}};
        %
        % ============ INSTRUCTIONS BOX ============
        \node[anchor=north, inner sep=0pt] at ([yshift=-13cm]current page.north) {%
            \begin{minipage}{0.72\textwidth}%
            \begin{tcolorbox}[
                enhanced,
                colback=white,
                colframe=funTeal!30,
                colbacktitle=funTeal!70,
                coltitle=white,
                fonttitle=\Large\bfseries\sffamily,
                title={\faPen\hspace{3mm}Before You Start\hspace{3mm}\faPen},
                halign title=center,
                arc=10pt,
                outer arc=10pt,
                boxrule=1.5pt,
                width=\textwidth,
                top=5mm, bottom=5mm,
                left=8mm, right=8mm,
                toptitle=4mm, bottomtitle=4mm,
                shadow={2mm}{-2mm}{0mm}{funTeal!8},
            ]
                \sffamily\normalsize
                \begin{itemize}[leftmargin=6mm, itemsep=4pt]
                    \item[\textcolor{funTeal}{\faCheck}] \textbf{Read each question carefully} before choosing your answer.
                    \item[\textcolor{funTeal}{\faCheck}] \textbf{Show your work} on scratch paper when you need to.
                    \item[\textcolor{funTeal}{\faCheck}] \textbf{Skip hard questions} and come back to them later.
                    \item[\textcolor{funTeal}{\faCheck}] \textbf{Check your answers} when you're done.
                    \item[\textcolor{funTeal}{\faCheck}] \textbf{Take your time} --- there's no rush!
                \end{itemize}
            \end{tcolorbox}%
            \end{minipage}%
        };%
        %
        % ============ ENCOURAGEMENT ============
        \node[
            font=\fontsize{16}{20}\selectfont\sffamily\bfseries\color{funTealDark},
        ] at ([yshift=5.5cm]current page.south)
            {\faStar\hspace{3mm}You've Got This!\hspace{3mm}\faStar};
        %
        \node[
            font=\normalsize\sffamily\color{funGray},
        ] at ([yshift=4.5cm]current page.south)
            {Do your best and show what you know!};
        %
        % ============ BOTTOM DECORATIONS ============
        \node[opacity=0.5] at ([xshift=-3cm, yshift=3cm]current page.south east)
            {\iconOwl[2cm]};
        \node[opacity=0.12] at ([xshift=3cm, yshift=2.5cm]current page.south west)
            {\textcolor{funTeal}{\fontsize{24}{26}\selectfont\faStar}};
        \node[opacity=0.08] at ([xshift=7cm, yshift=1.5cm]current page.south west)
            {\textcolor{funYellow}{\fontsize{18}{20}\selectfont\faStar}};
        %
        % Small accent dots
        \foreach \x/\y in {4.5/-2.5, 8/-1.2, 13.5/-3.5, 16/-1.8} {
            \fill[white, opacity=0.12]
                ([xshift=\x cm, yshift=\y cm]current page.north west) circle (2pt);
        }
        %
    \end{tikzpicture}%
    %
    \newpage
}

%-------------------------------------------
% TEST SCORE PAGE
%   Shown after each practice test before the next one.
%   #1 = test number
%   #2 = number of questions
%-------------------------------------------
\newcommand{\testScorePage}[2]{%
    \newpage
    \thispagestyle{empty}%
    \vspace*{\fill}
    \begin{center}
    \begin{tcolorbox}[
        enhanced,
        colback=funTealLight,
        colframe=funTeal!60,
        boxrule=2pt,
        arc=14pt,
        outer arc=14pt,
        width=0.82\linewidth,
        halign=center,
        top=10mm, bottom=10mm,
        shadow={2pt}{-2pt}{0pt}{funGray!30},
    ]
        {\fontsize{20}{24}\selectfont\bfseries\sffamily\color{funTealDark}%
            \faStar\hspace{3mm}End of Practice Test #1\hspace{3mm}\faStar%
        }\\[6mm]
        {\large\sffamily\color{funGrayDark}%
            Great job finishing the test!%
        }\\[8mm]
        %
        % --- Score tracking box ---
        \begin{tcolorbox}[
            enhanced,
            colback=white,
            colframe=funTeal!30,
            arc=8pt,
            boxrule=1pt,
            width=0.85\linewidth,
            top=5mm, bottom=5mm,
            left=6mm, right=6mm,
        ]
            \sffamily
            \begin{center}
                {\large\bfseries\color{funTealDark}\faClipboardCheck\hspace{2mm}My Score}\\[4mm]
                I got \rule[-2pt]{2cm}{0.5pt} out of #2 questions right.\\[4mm]
                \textcolor{funGray}{Check your answers in the \textbf{Answer Key} at the back of the book.}
            \end{center}
        \end{tcolorbox}%
        \vspace{4mm}
        {\sffamily\color{funGray}%
            \faLightbulb\hspace{2mm}Review any questions you missed. That's how we learn!%
        }
    \end{tcolorbox}
    \end{center}
    \vspace*{\fill}
    \newpage
}

%-------------------------------------------
% Toggle: set \hidesectionbannertrue in books where a custom
% title banner (e.g. \puzzlePageTitle) replaces the blue box.
%-------------------------------------------
\newif\ifhidesectionbanner
\hidesectionbannerfalse

%-------------------------------------------
% SECTION BANNER COMMAND (replaces standalone \topicTitle)
% Usage inside \titleformat: renders numbered blue banner with stars
%-------------------------------------------
\newcommand{\sectionBanner}[2]{%  % #1 = section number, #2 = title text
    \noindent
    \ifhidesectionbanner\else
    \begin{tcolorbox}[
        enhanced,
        colback=funBlue,
        colframe=funBlueDark,
        boxrule=0pt,
        arc=12pt,
        outer arc=12pt,
        top=5mm,
        bottom=5mm,
        left=8mm,
        right=8mm,
        width=0.85\linewidth,
        center,
        halign=center,
        fontupper=\Large\bfseries\sffamily\color{white},
        shadow={1mm}{-1mm}{0mm}{funBlueDark!50},
    ]
        \iconStar[0.7cm]\hspace{4mm}%
        #1\enspace #2%
        \hspace{4mm}\iconStar[0.7cm]%
    \end{tcolorbox}%
    \vspace{2mm}%
    \fi
}

%-------------------------------------------
% SECTION STYLING - Blue banner with section number and stars
%-------------------------------------------
\titleformat
{\section}
[block]
{}
{\sectionBanner{\thesection}{#1}}
{0pt}
{}
[]

\titleformat
{name=\section, numberless}
[block]
{\bfseries\sffamily\Large\color{funBlueDark}}
{#1}
{0cm}
{}
[]

\titlespacing*{\section}{0pt}{0pt}{0pt}

%-------------------------------------------
% PAGE BREAK BEFORE SECTIONS
% Must happen OUTSIDE \titleformat callback to avoid blank-page bug.
% Issuing \clearpage inside \sectionBanner (titlesec callback) causes
% an extra phantom page due to titlesec internals.
%-------------------------------------------
\AddToHook{cmd/section/before}{%
    \ifdim\pagetotal<50pt\else\newpage\fi
}

%-------------------------------------------
% SUBSECTION STYLING
%-------------------------------------------
\titleformat
{\subsection}
[block]
{\bfseries\sffamily\large\color{funGreenDark}}
{\llap{\textcolor{funGreen}{\thesubsection}\hspace{1em}}#1}
{0cm}
{}
[]

\titleformat
{name=\subsection, numberless}
[block]
{\bfseries\sffamily\large\color{funGreenDark}}
{#1}
{0cm}
{}
[]

\titlespacing*{\subsection}{0pt}{12pt}{4pt}

%-------------------------------------------
% SUBSUBSECTION STYLING
%-------------------------------------------
\titleformat
{\subsubsection}
[block]
{\bfseries\sffamily\color{funOrangeDark}}
{\llap{{\thesubsubsection}\hspace{1em}}#1}
{0cm}
{}
[]

\titleformat
{name=\subsubsection, numberless}
[block]
{\bfseries\sffamily\color{funOrangeDark}}
{#1}
{0cm}
{}
[]

\titlespacing*{\subsubsection}{0pt}{8pt}{4pt}

%-------------------------------------------
\titleformat
{\paragraph}
[runin]
{\bfseries\sffamily}
{}
{0cm}
{#1}
[]

\titlespacing*{\paragraph}{0pt}{0pt}{6pt}

%----------------------------------------------------------------------------------------
%   TABLE OF CONTENTS
%----------------------------------------------------------------------------------------
\usepackage{titletoc}
\setcounter{tocdepth}{2}
\contentsmargin{0cm}

% Chapter entries in TOC
\titlecontents{chapter}
[1.25cm]
{\addvspace{12pt}\large\sffamily\bfseries\hypersetup{linkcolor=funBlue}}
{\color{funBlue}\contentslabel[\Large\thecontentslabel]{1.25cm}}
{}
{\color{funBlue!60}\normalsize\;\titlerule*[6pt]{.}\;\color{funBlue}\thecontentspage}
[]

% Section entries in TOC
\titlecontents{section}
[1.25cm]
{\addvspace{3pt}\sffamily\bfseries}
{\contentslabel[\thecontentslabel]{1.45cm}}
{}
{~{\normalfont\titlerule*[6pt]{.}}~\thecontentspage}
[]

% Subsection entries in TOC
\titlecontents{subsection}
[1.25cm]
{\addvspace{1pt}\sffamily\small}
{\contentslabel[\thecontentslabel]{1.25cm}}
{}
{~\titlerule*[6pt]{.}~\thecontentspage}
[]

% Mini TOC entry format for chapter openers (prefix "l" used by \printcontents)
\titlecontents{lsection}[1.8em]
    {\addvspace{4pt}\sffamily\small}
    {\color{funBlueDark}\bfseries\contentslabel[\thecontentslabel]{1.8em}}
    {\hspace*{-1.8em}}
    {~{\normalfont\color{funGray!70}\titlerule*[6pt]{.}}~\color{funBlue}\bfseries\thecontentspage}

%----------------------------------------------------------------------------------------
%   FRIENDLY TABLE OF CONTENTS
%   Kid-friendly TOC showing only chapters and Answer Key.
%   Usage: \friendlyTOC  (place after initial pages, before \pagenumbering{arabic})
%----------------------------------------------------------------------------------------
\newcommand{\friendlyTOC}{%
    \newpage
    \thispagestyle{empty}%
    {%
    \sffamily
    %
    % --- Decorative top border ---
    \begin{center}
        \textcolor{funBlue!40}{%
            \foreach \i in {1,...,35}{\faStar\hspace{1pt}}%
        }
    \end{center}
    %
    \vspace{2mm}
    %
    % --- Title ---
    \begin{center}
        \textcolor{funBlueDark}{\fontsize{24}{28}\selectfont\bfseries
        \faStar~Table of Contents~\faStar}
    \end{center}
    %
    \vspace{2mm}
    %
    % --- Subtitle ---
    \begin{center}
        \textcolor{funGray}{\large Here's what we'll explore together!}
    \end{center}
    %
    \vspace{4mm}
    %
    % --- TOC box ---
    \begin{tcolorbox}[
        enhanced,
        colback=white,
        colframe=funBlue!35,
        arc=10pt,
        outer arc=10pt,
        boxrule=1.5pt,
        borderline={1.5pt}{2pt}{funBlue!20, dashed},
        left=8mm, right=8mm, top=6mm, bottom=6mm,
        shadow={2mm}{-2mm}{0mm}{funBlue!6},
    ]
        % Temporarily show only chapter-level entries
        {%
        \setcounter{tocdepth}{0}%
        \renewcommand{\contentsmargin}{0cm}%
        %
        % Override chapter format for this friendly TOC
        \titlecontents{chapter}
            [0cm]
            {\addvspace{8pt}\large\sffamily\bfseries\hypersetup{linkcolor=funBlue}}
            {\color{funBlue}\makebox[1.6cm][l]{\raisebox{-1pt}{\textcolor{funYellow}{\faStar}}~\Large\thecontentslabel}}
            {\color{funBlue}\raisebox{-1pt}{\textcolor{funYellow}{\faStar}}~}
            {\color{funBlue!50}\normalsize\;\titlerule*[6pt]{.}\;\color{funBlue}\thecontentspage}
            []
        %
        \@starttoc{toc}%
        }%
    \end{tcolorbox}%
    %
    \vspace{6mm}
    %
    % --- Owl encouragement ---
    \begin{center}
        \iconOwl[1.2cm]\hspace{4mm}%
        \raisebox{0.35cm}{%
            \textcolor{funBlueDark}{\large\bfseries Let's learn and have fun!}%
        }
    \end{center}
    %
    % --- Decorative bottom border ---
    \vfill
    \begin{center}
        \textcolor{funBlue!40}{%
            \foreach \i in {1,...,35}{\faStar\hspace{1pt}}%
        }
    \end{center}
    }%
    % No \newpage here: the following \chapter{} issues \clearpage which
    % properly flushes this TOC page without creating a blank page in between.
}

%----------------------------------------------------------------------------------------
%   TABLES
%----------------------------------------------------------------------------------------
\usepackage{array}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\usepackage{booktabs}

%----------------------------------------------------------------------------------------
%   LISTS - Kid-friendly markers
%----------------------------------------------------------------------------------------
\usepackage{enumitem}
\setlist{nolistsep, noitemsep}

\renewcommand{\labelenumi}{\textbf{\color{funBlue}\arabic{enumi}.}}
\renewcommand{\labelenumii}{\textbf{\color{funGreen}\alph{enumii}.}}
\renewcommand{\labelenumiii}{\textbf{\color{funOrange}\roman{enumiii}.}}

\renewcommand{\labelitemi}{\textcolor{funBlue}{\raisebox{0pt}{\large$\bullet$}}}
\renewcommand{\labelitemii}{\textcolor{funGreen}{--}}
\renewcommand{\labelitemiii}{\textcolor{funOrange}{$\circ$}}

% Fun checkmark for special lists
\newcommand{\mycheckmark}{\textcolor{funGreen}{\raisebox{-0.1em}{\faCheck}}}

%----------------------------------------------------------------------------------------
%   LINKS
%----------------------------------------------------------------------------------------
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    urlcolor=funBlue,
    linkcolor=black,
    citecolor=funBlue,
    hyperindex=true,
    linktoc=all,
}

%----------------------------------------------------------------------------------------
%   BOOKMARKS
%----------------------------------------------------------------------------------------
\usepackage{bookmark}
\bookmarksetup{
    open,
    numbered,
    addtohook={%
        \ifnum\bookmarkget{level}=0
            \bookmarksetup{bold}
        \fi
    }
}

%----------------------------------------------------------------------------------------
%   MATH SUPPORT
%----------------------------------------------------------------------------------------
\usepackage{amsmath, amsfonts, amssymb}

%----------------------------------------------------------------------------------------
%   TIKZ
%----------------------------------------------------------------------------------------
\usepackage{tikz}
\usetikzlibrary{
    arrows.meta,
    shapes.geometric,
    shapes.multipart,
    calc,
    math,
    positioning,
    decorations.pathmorphing,
    decorations.markings,
    patterns,
}

%----------------------------------------------------------------------------------------
%   TITLE PAGE
%----------------------------------------------------------------------------------------
\renewcommand{\titlepage}[2]{
    \thispagestyle{empty}
    \begin{tikzpicture}[remember picture, overlay]
        \node [inner sep=0pt] at (current page.center) {#1};
        \node [anchor=north, inner sep=1.25cm, rectangle, fill=funBlue!20, fill opacity=0, text opacity=1, minimum height=0.2\paperheight, minimum width=\paperwidth, text width=0.8\paperwidth] at ([yshift=-1.25cm]current page.north) {#2};
    \end{tikzpicture}
}

% Title environments
\newenvironment{bookTitle}
    {\par\vspace*{5mm}\centering\color{funBlueDark}\Huge\bfseries}
    {\par\vspace{5mm}}

\newenvironment{subtitle}
    {\par\vspace*{0mm}\centering\itshape\fontsize{18pt}{24pt}\selectfont}
    {\par\vspace*{5mm}}

\newenvironment{section-title}
    {\par\vspace*{5mm}\centering\color{funBlue}\LARGE\bfseries}
    {\par\vspace{5mm}}

%----------------------------------------------------------------------------------------
%   TITLE PAGE MACROS (for copyright_page.tex)
%----------------------------------------------------------------------------------------
\providecommand{\VMBookTitle}{Grade 7 Math Made Easy}
\providecommand{\VMBookSubtitle}{}

%----------------------------------------------------------------------------------------
%   LOAD GRADE 4 FUN PACKAGES
%   These provide all the colorful, kid-friendly environments.
%----------------------------------------------------------------------------------------
\RequirePackage{VM_packages/VMfunTeaching}    % Topic titles, concepts, steps, rules, vocabulary
\RequirePackage{VM_packages/VMfunExamples}    % Worked examples, solutions, answer highlights
\RequirePackage{VM_packages/VMfunPractice}    % Practice, challenges, show work, quick check
\RequirePackage{VM_packages/VMfunExtras}      % Mascot, tips, fun facts, warnings
\RequirePackage{VM_packages/VMfunMath}        % Place value, column arithmetic, number lines, visuals
\RequirePackage{VM_packages/VMfunAnswers}      % Answer key: \answer, \answerExplain, \answerTF, etc.
\RequirePackage{VM_packages/VMfunSteps}       % Step-by-step teaching environments
\RequirePackage{VM_packages/VMfunQuiz}        % Quiz environments: quizPage, quizQ, bonusChallenge
\RequirePackage{VM_packages/VMfunPuzzles}     % Puzzle & brain teaser environments
\RequirePackage{VM_packages/VMfunWorksheet}   % Worksheet activity environments
\RequirePackage{VM_packages/VMfunCover}       % Cover page with state name overlay

\providecommand{\degree}{\ensuremath{^\circ}}   % degree symbol, works in text and math mode
