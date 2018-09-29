FROM tensorflow/tensorflow:latest-py3

# Install R
RUN apt update
RUN apt install apt-transport-https ed libgit2-dev libssl-dev -y
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/'
RUN apt update
RUN apt install r-base -y

# Install R packages
RUN R -e "install.packages(\
    c('ggplot2',\
      'faraway',\      
      'repr',\
      'IRdisplay',\
      'evaluate',\
      'crayon',\
      'pbdZMQ',\
      'devtools',\
      'uuid',\
      'digest'),\
    repos='http://cran.us.r-project.org');\
    devtools::install_github('IRkernel/IRkernel');\
    IRkernel::installspec(user=FALSE);"
