Adding new cli commands
All cli-related functions are located in pkg/cmd
.
Each cli command usually calls a function in another package.
For example, the vikunja migrate
command calls migration.Migrate()
.
Vikunja uses the amazing cobra library for its cli. Please refer to its documentation for information about how to use flags etc.
To add a new cli command, add something like the following:
func init() {
rootCmd.AddCommand(myCmd)
}
var myCmd = &cobra.Command{
Use: "My-command",
Short: "A short description about your command.",
Run: func(cmd \*cobra.Command, args []string) {
// Call other functions
},
}
