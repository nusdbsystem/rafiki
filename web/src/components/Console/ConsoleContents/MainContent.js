import React from "react"
import PropTypes from "prop-types"
import { compose } from "redux"
import { Link, withRouter } from "react-router-dom"

import Paper from "@material-ui/core/Paper"
import { withStyles } from "@material-ui/core/styles"

// zoom addicon
import Fab from "@material-ui/core/Fab"
import Zoom from "@material-ui/core/Zoom"
import ListDSIcon from "@material-ui/icons/FormatListBulleted"
import AddIcon from "@material-ui/icons/Add"

const styles = theme => ({
  paper: {
    maxWidth: 936,
    margin: "auto",
    overflow: "hidden",
    marginBottom: 20,
    position: "relative",
    paddingBottom: 80,
  },
  fab: {
    position: "absolute",
    bottom: theme.spacing(3),
    right: theme.spacing(3),
    zIndex: 10,
  },
  extendedIcon: {
    marginRight: theme.spacing(1),
  },
})

class MainContent extends React.Component {
  static propTypes = {
    classes: PropTypes.object.isRequired,
    children: PropTypes.node,
    location: PropTypes.object,
  }

  render() {
    const { classes, children, location } = this.props
    return (
      <Paper className={classes.paper}>
        {children}
        {location.pathname === "/console/datasets/list-dataset" ? (
          <Zoom in={true} unmountOnExit>
            <Fab
              className={classes.fab}
              color="primary"
              component={Link}
              to="/console/datasets/upload-datasets"
            >
              <AddIcon />
            </Fab>
          </Zoom>
        ) : (
          <Zoom in={true} unmountOnExit>
            <Fab
              variant="extended"
              className={classes.fab}
              color="primary"
              component={Link}
              to="/console/datasets/list-dataset"
            >
              <ListDSIcon className={classes.extendedIcon} />
              List Dataset
            </Fab>
          </Zoom>
        )}
      </Paper>
    )
  }
}

export default compose(withRouter, withStyles(styles))(MainContent)
