__author__ = 'Liam'

import types

def flag(func):
    func.is_flag = True
    return func



class BadSearchOp(Exception):
    def __init__(self, value = "bad search operation"):
        self.value = value
    def __str__(self):
        return "BadSearchOp: %s" % self.value


class ImapSearchQueryParser(object):
    """
    Receives a list of commands for the IMAP V4 serach
    and returns a dictionary of the commands, that can be used in various mail API's
    including walla API for mail

    based on RFC3501:
    https://tools.ietf.org/html/rfc3501#section-6.4.4


    example of commands:
    C: A282 SEARCH FLAGGED SINCE 1-Feb-1994 NOT FROM "Smith"
    S: * SEARCH 2 84 882
    S: A282 OK SEARCH completed
    C: A283 SEARCH TEXT "string not in mailbox"
    S: * SEARCH
    S: A283 OK SEARCH completed
    C: A284 SEARCH CHARSET UTF-8 TEXT {6}
    C: XXXXXX
    S: * SEARCH 43
    S: A284 OK SEARCH completed


    """

    def __init__(self):
        """

        :param query:
        :return:
        """

        #self.log("{} constructor ".format(self.__class__.__name__))

        self.opFunctionList = [x for x,y in self.__class__.__dict__.items() if type(y) == types.FunctionType]
        self.query = None
        self.commands = {}
        self.commands_list = []

        #self.__validate()

    #########################################################################
    #
    def __repr__(self):
        return self.__class__.__name__+", commands: %s" % self.commands


    def log(self,msg):
        print msg
        #self.logger.log(logging.DEBUG,msg)


    def __str__(self):
        return str(self.commands)


    def _update_command_list(self, command, idx1, idx2=None):
        """
        Updates both the command list and commands as to prepare for OR parsing
        :param command: a single dictionary object with one key:value (command:argument)
        :param idx1: first index
        :param idx2: second index
        :return:
        """

        command_wrapper = {
            'data': command,
            'pos': [idx1]
        }

        # update second position
        if idx2:
            command_wrapper['pos'].append(idx2)

        # adding to command list with positions of current command and argument
        self.commands_list.append(command_wrapper)
        # update the command
        self.commands.update(command)


    @flag
    def OP__ALL(self,currentIndex=None):
        self._update_command_list({'all': True}, currentIndex)

    @flag
    def OP__ANSWERED(self,currentIndex=None):
        self._update_command_list({'answered': True}, currentIndex)

    def OP__BCC(self,currentIndex=None):
        """
        BCC <string>
         Messages that contain the specified string in the envelope
         structure's BCC field.
        :param currentIndex:
        :return:
        """
        if currentIndex+1 < len(self.query):
            #todo check bcc validation
            self._update_command_list({'bcc': self.query[currentIndex+1]}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "BCC" provided but with no argument in query list')


    def OP__BEFORE(self,currentIndex=None):
        argument = self._get_command_argument(currentIndex)
        if argument:
            self._update_command_list({'before': argument}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "BEFORE" provided but with no argument in query list')

    def OP__BODY(self,currentIndex=None):
        argument = self._get_command_argument(currentIndex)
        if argument:
            self._update_command_list({'body': argument}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "BODY" provided but with no argument in query list')


    def OP__CC(self,currentIndex=None):
        argument = self._get_command_argument(currentIndex)
        if argument:
            self._update_command_list({'cc': argument}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "CC" provided but with no argument in query list')



    @flag
    def OP__DELETED(self,currentIndex=None):
        self._update_command_list({'deleted': True}, currentIndex)

    @flag
    def OP__DRAFT(self,currentIndex=None):
        self._update_command_list({'draft': True}, currentIndex)

    @flag
    def OP__FLAGGED(self,currentIndex=None):
        self._update_command_list({'flagged': True}, currentIndex)

    def OP__FROM(self,currentIndex=None):
        """
        FROM <string>
         Messages that contain the specified string in the envelope
         structure's FROM field.
        :return:
        """

        # assuming that next item is the value, such as: FROM 'man@mayman.com'
        argument = self._get_command_argument(currentIndex)
        if argument:
            self._update_command_list({'from': argument}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "FROM" provided but with no argument in query list')



    def OP__HEADER(self,currentIndex=None):
        # todo work on this one
        pass

    def OP__KEYWORD(self,currentIndex=None):
        argument = self._get_command_argument(currentIndex)
        if argument:
            self._update_command_list({'keyword': argument}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "KEYWORD" provided but with no argument in query list')


    def OP__LARGER(self,currentIndex=None):
        argument = self._get_command_argument(currentIndex)
        if argument:
            self._update_command_list({'larger': argument}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "LARGER" provided but with no argument in query list')


    @flag
    def OP__NEW(self,currentIndex=None):
        self._update_command_list({'new': True}, currentIndex)


    @flag
    def OP__OLD(self,currentIndex=None):
        self._update_command_list({'old': True}, currentIndex)

    @flag
    def OP__RECENT(self,currentIndex=None):
        self._update_command_list({'recet': True}, currentIndex)

    @flag
    def OP__SEEN(self,currentIndex=None):
        self._update_command_list({'seen': True}, currentIndex)

    @flag
    def OP__UNANSWERED(self,currentIndex=None):
        self._update_command_list({'unanswered': True}, currentIndex)

    @flag
    def OP_UNDRAFT(self,currentIndex=None):
        self._update_command_list({'undraft': True}, currentIndex)

    @flag
    def OP__UNFLAGGED(self,currentIndex=None):
        self._update_command_list({'unflagged': True}, currentIndex)

    @flag
    def OP__UNKEYWORD(self,currentIndex=None):
        """
        UNKEYWORD <flag>
         Messages that do not have the specified keyword flag set.
        """
        # todo make it proper somehow
        #self.commands.update({'seen': True})

    @flag
    def OP__UNSEEN(self,currentIndex=None):
        self._update_command_list({'unseen': True}, currentIndex)


    def OP__SENTBEFORE(self,currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'sentbefore': self.query[currentIndex+1]}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "SENTBEFORE" provided but with no argument in query list')

    def OP__SENTON(self, currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'senton': self.query[currentIndex+1]}, currentIndex)
        else:
            raise BadSearchOp('Operator "SENTON" provided but with no argument in query list')

    def OP__SENTSINCE(self,currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'sentsince': self.query[currentIndex+1]},currentIndex)
        else:
            raise BadSearchOp('Operator "SENTSINCE" provided but with no argument in query list')

    def OP__SINCE(self,currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'since': self.query[currentIndex+1]}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "SINCE" provided but with no argument in query list')

    def OP__SMALLER(self,currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'smaller': self.query[currentIndex+1]}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "SMALLER" provided but with no argument in query list')

    def OP__SUBJECT(self,currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'subject': self.query[currentIndex+1]}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "SUBJECT" provided but with no argument in query list')

    def OP__TEXT(self,currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'text': self.query[currentIndex+1]}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "TEXT" provided but with no argument in query list')

    def OP__TO(self,currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'to': self.query[currentIndex+1]}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "TO" provided but with no argument in query list')

    def OP__UID(self,currentIndex=None):
        if currentIndex+1 < len(self.query):
            self._update_command_list({'uid': self.query[currentIndex+1]}, currentIndex, currentIndex+1)
        else:
            raise BadSearchOp('Operator "UID" provided but with no argument in query list')


    def _NOT_PARSER(self):
        #print "NOT PARSER---"
        for i in range(len(self.query)):
            operator = self.query[i]
            #print "operator:"+operator
            if (operator=="NOT"):
                #print "found NOT index:{}".format(i)
                # find what is next command
                if (i+1<len(self.query)):
                    next_possible_command = self.query[i+1]
                    #print "next_possible_command:{}".format(next_possible_command)
                    # is possible command a valid operator function?
                    possible_command_function = self.__get_op_function(next_possible_command)
                    # indeed a function
                    if (callable(possible_command_function)):
                        is_flag = getattr(possible_command_function,'is_flag',False)
                        if is_flag:
                            command = {next_possible_command.lower(): False}
                            self._update_command_list(command,i)
                        else:
                            old_operator_value = self.commands.get(next_possible_command.lower())
                            for command in self.commands_list:
                                if command['data'].get(next_possible_command.lower(),None):
                                    del command['data']
                                    command['data'] = {
                                        'not-'+next_possible_command.lower():old_operator_value
                                    }
                                    # add the from position so it will be match when doing OR NOT
                                    command['pos'].append(i)

                            self.commands['not-'+next_possible_command.lower()] = old_operator_value
                            del self.commands[next_possible_command.lower()]




    def _OR_PARSER(self):
        """
        we start parsing the OR command and dialectically correct / update the commands using the commands_list metadata
        :return:
        """

        def _find_command_by_indexes(index1,index2):
            #for i in range(len(self.commands_list)):
            foundCommands = []
            for command in self.commands_list:
                pos = command['pos']
                #print "command:{}".format(command)
                if (index1 in pos):
                    foundCommands.append(command['data'])
                if (index2 in pos):
                    foundCommands.append(command['data'])

            #print "Found OR commands: {}".format(foundCommands)
            return foundCommands


        for i in range(len(self.query)):
            operator = self.query[i]
            rhs,lhs = None,None
            if operator== "OR":

                if (i+1<len(self.query)):
                    rhs = i+1
                if i-1 > -1:
                    lhs = i-1
                # only if both rhs and lhs exist can we go on
                if not rhs and not lhs:
                    raise BadSearchOp('Operator "OR" provided but missing both left hand and right hand side params')

                or_commands = _find_command_by_indexes(lhs,rhs)
                if len(or_commands)==2:
                    orDict = {}
                    for command in or_commands:
                        #orDict.update(command)
                        # if command in commands
                        for k,v in command.iteritems():
                            #print "K:{} v:{}".format(k,v)
                            # key of command found
                            if k in self.commands:
                                orDict[k] = v
                                del self.commands[k]

                    #print "orDict:{}".format(orDict)

                    self.commands['or'] = orDict
                    #if command in self.commands



                #print "OR RHS:{} LHS:{}".format(rhs, lhs)







    def _get_command_argument(self,currentIndex):
        """
        will treat the next command as argument to command in currentIndex.
        used for all commands that have parameters (arguments),
        such as:
        FROM <string>
        BEFORE <date>
        BODY <string> etc...
        :param currentIndex:
        :return:
        """
        # assuming that next item is the value, such as: FROM 'man@mayman.com'
        if currentIndex+1 < len(self.query):
            #todo check validation
            argument = self.query[currentIndex+1]
            return argument
        else:
            return None

    @property
    def opList(self):
        return self.opFunctionList

    def __get_op_function(self,operator):
        operatorFuncName = "OP__"+operator.upper()
        if operatorFuncName in self.opList:
            opFunction = getattr(self,operatorFuncName)
            return opFunction
        else:
            return None

    def __validate(self):
        """
        tries to validate the command set
        :return:
        """
        print "IMAP4 Search Query List:{}".format(self.query)
        if len(self.query) < 1:
            raise BadSearchOp("not enough items in list, has to be more then 1 (sequence set,search)")


        for i in range(len(self.query)):
            operator = self.query[i]
            opFunction = self.__get_op_function(operator)
            if (opFunction):
                #print "operator found:{}".format(operator)
                opFunction(i)
            else:
                pass
                #print "operator not found:{}".format(operator)


        self._NOT_PARSER()
        self._OR_PARSER()

        return self.commands

    def parse(self, query):
        self.query = query
        return self.__validate()



if __name__ == "__main__":

    test_commands = [
        ['NOT','FLAGGED','SINCE','1-Feb-1994','NOT','FROM','Smith','BCC', 'aaaa@aaaa.net.il'],
        ['NOT','BEFORE','1-Feb-1994','NOT','FROM','Smith'],
        ['SEEN','BEFORE','1-Feb-1994','OR','NOT','FROM','Smith'],
        ['NOT','SENTBEFORE','1-Feb-1994','NOT','FROM','Smith'],
        ['SUBJECT','all about love','NOT','TO','aaaa@aaaa.net.il','SINCE','1-Feb-1994','NOT','FROM','Smith','UID','1:*','OR','NOT','TEXT','Go To Hello'],
        ['SEEN','BEFORE','1-Feb-1994','OR','NOT','FROM','Smith']
    ]

    for command_set in test_commands:
        c = ImapSearchQueryParser()
        res = c.parse(command_set)
        print "Result:{}".format(res)


    #print "command_list:{}".format(c.commands_list)