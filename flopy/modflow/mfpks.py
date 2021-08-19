"""
mfpks module.  Contains the ModflowPks class. Note that the user can access
the ModflowPks class as `flopy.modflow.ModflowPks`.

"""
import sys
from ..pakbase import Package


class ModflowPks(Package):
    """
    MODFLOW Pks Package Class.

    Parameters
    ----------
    model : model object
        The model object (of type :class:`flopy.modflow.mf.Modflow`) to which
        this package will be added.
    mxiter : int
        maximum number of outer iterations. (default is 100)
    innerit : int
        maximum number of inner iterations. (default is 30)
    hclose : float
        is the head change criterion for convergence. (default is 1.e-3).
    rclose : float
        is the residual criterion for convergence. (default is 1.e-1)
    relax : float
        is the relaxation parameter used with npcond = 1. (default is 1.0)
    .
    .
    .
    iprpks : int
        solver print out interval. (default is 0).
    mutpks : int
        If mutpcg = 0, tables of maximum head change and residual will be
            printed each iteration.
        If mutpcg = 1, only the total number of iterations will be printed.
        If mutpcg = 2, no information will be printed.
        If mutpcg = 3, information will only be printed if convergence fails.
            (default is 3).
    damp : float
        is the steady-state damping factor. (default is 1.)
    dampt : float
        is the transient damping factor. (default is 1.)
    extension : list string
        Filename extension (default is 'pks')
    unitnumber : int
        File unit number (default is 27).
    filenames : str or list of str
        Filenames to use for the package. If filenames=None the package name
        will be created using the model name and package extension. If a
        single string is passed the package will be set to the string.
        Default is None.

    Attributes
    ----------

    Methods
    -------

    See Also
    --------

    Notes
    -----

    Examples
    --------

    >>> import flopy
    >>> m = flopy.modflow.Modflow()
    >>> pks = flopy.modflow.ModflowPks(m)

    """

    def __init__(
        self,
        model,
        mxiter=100,
        innerit=50,
        isolver=1,
        npc=2,
        iscl=0,
        iord=0,
        ncoresm=1,
        ncoresv=1,
        damp=1.0,
        dampt=1.0,
        relax=0.97,
        ifill=0,
        droptol=0.0,
        hclose=1e-3,
        rclose=1e-1,
        l2norm=None,
        iprpks=0,
        mutpks=3,
        mpi=False,
        partopt=0,
        novlapimpsol=1,
        stenimpsol=2,
        verbose=0,
        partdata=None,
        extension="pks",
        unitnumber=None,
        filenames=None,
    ):
        """
        Package constructor.

        """
        # set default unit number of one is not specified
        if unitnumber is None:
            unitnumber = ModflowPks._defaultunit()

        # set filenames
        if filenames is None:
            filenames = [None]
        elif isinstance(filenames, str):
            filenames = [filenames]

        # Fill namefile items
        name = [ModflowPks._ftype()]
        units = [unitnumber]
        extra = [""]

        # set package name
        fname = [filenames[0]]

        # Call ancestor's init to set self.parent, extension, name and unit number
        Package.__init__(
            self,
            model,
            extension=extension,
            name=name,
            unit_number=units,
            extra=extra,
            filenames=fname,
        )
        # check if a valid model version has been specified
        if model.version == "mf2k" or model.version == "mfnwt":
            err = "Error: cannot use {} package with model version {}".format(
                self.name, model.version
            )
            raise Exception(err)

        self._generate_heading()
        self.url = "pks.htm"
        self.mxiter = mxiter
        self.innerit = innerit
        self.isolver = isolver
        self.npc = npc
        self.iscl = iscl
        self.iord = iord
        self.ncoresm = ncoresm
        self.ncoresv = ncoresv
        self.damp = damp
        self.dampt = dampt
        self.relax = relax
        self.ifill = ifill
        self.droptol = droptol
        self.hclose = hclose
        self.rclose = rclose
        self.l2norm = l2norm
        self.iprpks = iprpks
        self.mutpks = mutpks
        # MPI
        self.mpi = mpi
        self.partopt = partopt
        self.novlapimpsol = novlapimpsol
        self.stenimpsol = stenimpsol
        self.verbose = verbose
        self.partdata = partdata

        self.parent.add_package(self)

    def write_file(self):
        """
        Write the package file.

        Returns
        -------
        None

        """
        # Open file for writing
        f = open(self.fn_path, "w")
        f.write("%s\n" % self.heading)
        f.write("MXITER {0}\n".format(self.mxiter))
        f.write("INNERIT {0}\n".format(self.innerit))
        f.write("ISOLVER {0}\n".format(self.isolver))
        f.write("NPC {0}\n".format(self.npc))
        f.write("ISCL {0}\n".format(self.iscl))
        f.write("IORD {0}\n".format(self.iord))
        if self.ncoresm > 1:
            f.write("NCORESM {0}\n".format(self.ncoresm))
        if self.ncoresv > 1:
            f.write("NCORESV {0}\n".format(self.ncoresv))
        f.write("DAMP {0}\n".format(self.damp))
        f.write("DAMPT {0}\n".format(self.dampt))
        if self.npc > 0:
            f.write("RELAX {0}\n".format(self.relax))
        if self.npc == 3:
            f.write("IFILL {0}\n".format(self.ifill))
            f.write("DROPTOL {0}\n".format(self.droptol))
        f.write("HCLOSEPKS {0}\n".format(self.hclose))
        f.write("RCLOSEPKS {0}\n".format(self.rclose))
        if self.l2norm != None:
            if self.l2norm.lower() == "l2norm" or self.l2norm == "1":
                f.write("L2NORM\n")
            elif self.l2norm.lower() == "rl2norm" or self.l2norm == "2":
                f.write("RELATIVE-L2NORM\n")
        f.write("IPRPKS {0}\n".format(self.iprpks))
        f.write("MUTPKS {0}\n".format(self.mutpks))
        # MPI
        if self.mpi:
            f.write("PARTOPT {0}\n".format(self.partopt))
            f.write("NOVLAPIMPSOL {0}\n".format(self.novlapimpsol))
            f.write("STENIMPSOL {0}\n".format(self.stenimpsol))
            f.write("VERBOSE {0}\n".format(self.verbose))
            if self.partopt == 1 | 2:
                pass
                # to be implemented

        f.write("END\n")
        f.close()

    @classmethod
    def load(cls, f, model, ext_unit_dict=None):
        """
        Load an existing package.

        Parameters
        ----------
        f : filename or file handle
            File to load.
        model : model object
            The model object (of type :class:`flopy.modflow.mf.Modflow`) to
            which this package will be added.
        ext_unit_dict : dictionary, optional
            If the arrays in the file are specified using EXTERNAL,
            or older style array control records, then `f` should be a file
            handle.  In this case ext_unit_dict is required, which can be
            constructed using the function
            :class:`flopy.utils.mfreadnam.parsenamefile`.

        Returns
        -------
        pks : ModflowPks object

        Examples
        --------

        >>> import flopy
        >>> m = flopy.modflow.Modflow()
        >>> pks = flopy.modflow.ModflowPks.load('test.pks', m)

        """

        if model.verbose:
            sys.stdout.write("loading pks package file...\n")

        openfile = not hasattr(f, "read")
        if openfile:
            filename = f
            f = open(filename, "r")

        # dataset 0 -- header

        print(
            "   Warning: "
            "load method not completed. default pks object created."
        )

        if openfile:
            f.close()

        # set package unit number
        unitnumber = None
        filenames = [None]
        if ext_unit_dict is not None:
            unitnumber, filenames[0] = model.get_ext_dict_attr(
                ext_unit_dict, filetype=ModflowPks._ftype()
            )

        return cls(model, unitnumber=unitnumber, filenames=filenames)

    @staticmethod
    def _ftype():
        return "PKS"

    @staticmethod
    def _defaultunit():
        return 27
